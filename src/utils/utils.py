

import re
import math
import ffmpeg
from pytube.exceptions import RegexMatchError
from urllib.parse import urlparse, parse_qs
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import threading
from post_request2db import post_to_db
from src.constant import *


def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    # logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            # logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )


def extract_audio(yt_id: str):
    extracted_audio = f"{AUDIOS_PATH}audio-{yt_id}.wav"
    stream = ffmpeg.input(f"{VIDEOS_PATH}{yt_id}")

    stream = ffmpeg.output(stream, extracted_audio)
    try:
        ffmpeg.run(stream, overwrite_output=True)
    except ffmpeg.Error as e:
        print(e.stderr)
    return extracted_audio


def get_param(url: str, key: str):
    parsed_url = urlparse(url)
    captured = parse_qs(parsed_url.query)[key][0]
    return captured


def transcribe(audio, dest: str = 'en'):
    model = WhisperModel(MODEL, device=DEVICE, compute_type="float32")
    segments, info = model.transcribe(audio)
    language = info[0]
    print(f" Transcription Language: {language}")
    print(f" Translated into: {dest}")

    segments = list(segments)
    translated_text_list = []

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    
    if language != dest:
        translator = GoogleTranslator(target=dest)
        for segment in segments:
            translated_text = translator.translate(segment.text)
            translated_text_list.append(translated_text)

            print("[%.2fs -> %.2fs] %s" %
                  (segment.start, segment.end, translated_text))
            
    return language,dest, segments,translated_text_list


def format_time_for_srt(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"

    return formatted_time

def generate_subtitle_file(yt_id: str, language, video_language, segments):
    subtitle_file = f"{SUBTITLES}sub-{yt_id}.{language}.srt"
    text = ""
    video_content = {"timeLine": {}}  # Khởi tạo timeLine là một từ điển rỗng

    for index, segment in enumerate(segments):
        segment_start = format_time_for_srt(segment['start'])
        segment_end = format_time_for_srt(segment['end'])

        # Cập nhật nội dung file SRT
        text += f"{str(index + 1)}\n"
        text += f"{segment_start} --> {segment_end}\n"
        text += f"{segment['text']}\n"
        try:
            text += f"{segment['translated_text_list'][index]}\n\n"
        except IndexError:
            print("No translated_text_list available for this segment")

        time_key = f"{segment_start} --> {segment_end}"
        if time_key not in video_content["timeLine"]:
            video_content["timeLine"][time_key] = {}

        video_content["timeLine"][time_key][video_language] = segment['text']
        try:
            video_content["timeLine"][time_key][language] = segment['translated_text_list'][index]
        except IndexError:
            print("No translation available for this segment")


    with open(subtitle_file, "w", encoding='utf-8') as f:
        f.write(text)

    return subtitle_file,video_content


def add_subtitle_to_video(yt_id: str, subtitle_file, subtitle_language):
    video_input_stream = ffmpeg.input(f"{VIDEOS_PATH}{yt_id}")
    # subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"{OUTPUT}output-{yt_id}-{subtitle_language}.mp4"
    # subtitle_track_tile = subtitle_file.replace(".srt", "")
    stream = ffmpeg.output(video_input_stream, output_video,
                           vf=f"subtitles={subtitle_file}")
    ffmpeg.run(stream, overwrite_output=True)
    file_path = post_to_db(output_video)
    print("Post to db thanh cong")
    return file_path