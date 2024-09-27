
# tasks.py
import pytube
from pytube. innertube import _default_clients
from pytube import cipher
from src.constant import VIDEOS_PATH
from src.utils.utils import extract_audio, transcribe, generate_subtitle_file, add_subtitle_to_video, get_throttling_function_name

# config
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

cipher.get_throttling_function_name = get_throttling_function_name


def download_video(url):
    yt = pytube.YouTube(url)
    yt_id = yt.video_id
    yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download(output_path=VIDEOS_PATH, filename=yt_id)
    return {"title": yt.title, "id": yt_id, "status": "completed"}


def extract_audio_task(clip_id,yt_id):
    audio_extract = extract_audio(clip_id,yt_id)
    return audio_extract, clip_id


def transcribe_task(audio_extract, clip_id, dest,yt_id):
    language, segments,translated_text_list = transcribe(audio_extract, dest)
    serializable_segments = []
    if len(translated_text_list) == 0:
       for segment in segments:
        serializable_segments.append({
            'start': segment.start,
            'end': segment.end,
            'text': segment.text
        })
    else : 
        for segment in segments:
            serializable_segments.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
                'translated_text_list': translated_text_list
            })

   
    
    return language, serializable_segments, clip_id


def generate_subtitle_file_task(language, segments_data, yt_id):
    subtitle_file = generate_subtitle_file(yt_id, language, segments_data)
    return subtitle_file, language, yt_id

def add_subtitle_to_video_task(subtitle_file, language, clip_id,yt_id):
  
    add_subtitle_to_video(clip_id, subtitle_file, language,yt_id)
    return f"Subtitle for {clip_id} added"