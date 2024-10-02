
# tasks.py
import pytube
from pytube. innertube import _default_clients
from pytube import cipher
from src.constant import VIDEOS_PATH
from src.utils.utils import extract_audio, transcribe, generate_subtitle_file, add_subtitle_to_video, get_throttling_function_name
import requests
import urllib.request

# config
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

cipher.get_throttling_function_name = get_throttling_function_name

import urllib.request
import pytube

def download_video(url):

    if "youtube.com" not in url:
        id = url.split('/')[-1].split('.')[0]
        urllib.request.urlretrieve(url, f'{VIDEOS_PATH}{id}')
        return {"title": "Non-YouTube Video", "id": f"{id}", "status": "completed"}
    else:
        yt = pytube.YouTube(url)
        yt_id = yt.video_id
        yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(output_path=VIDEOS_PATH, filename=yt_id)
        return {"title": yt.title, "id": yt_id, "status": "completed"}
def redownload_video(url):

    if "youtube.com" not in url:
        id = url.split('/')[-1].split('.')[0]
        urllib.request.urlretrieve(url, f'{VIDEOS_PATH}re-{id}')
        return {"title": "Non-YouTube Video", "id": f"{id}", "status": "completed"}
    else:
        yt = pytube.YouTube(url)
        yt_id = yt.video_id
        yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(output_path=VIDEOS_PATH, filename="re-"+yt_id)
        return {"title": yt.title, "id": yt_id, "status": "completed"}
    
def extract_audio_task(yt_id):
    audio_extract = extract_audio(yt_id)
    return audio_extract, yt_id


def transcribe_task(audio_extract, yt_id, dest):
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
        index = 0
        for segment in segments:
            
            serializable_segments.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
                'translated_text': translated_text_list[index]
            })
            index += 1

   
    
    return language, serializable_segments, yt_id


def generate_subtitle_file_task(language, segments_data, yt_id):
    subtitle_file = generate_subtitle_file(yt_id, language, segments_data)
    return subtitle_file, language, yt_id

def add_subtitle_to_video_task(subtitle_file, language, yt_id):
  
    file_path = add_subtitle_to_video(yt_id, subtitle_file, language)
    return file_path