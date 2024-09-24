# import os
# import uvicorn
# from celery import chain
# from fastapi import FastAPI
# from celery.result import AsyncResult

# from src.models.models import Item
# from src.utils.utils import *
# from src.constant import *

# from tasks import download_video, extract_audio_task, transcribe_task, generate_subtitle_file_task, add_subtitle_to_video_task
# from config import Config

# import pytube
# from pytube. innertube import _default_clients
# from pytube import cipher
# from src.constant import VIDEOS_PATH

# from src.utils.utils import extract_audio, transcribe, generate_subtitle_file, add_subtitle_to_video, get_throttling_function_name




# # Create necessary directories
# os.makedirs(AUDIOS_PATH, exist_ok=True)
# os.makedirs(VIDEOS_PATH, exist_ok=True)
# os.makedirs(SUBTITLES, exist_ok=True)
# os.makedirs(OUTPUT, exist_ok=True)

# app = FastAPI()

# # def download_video(url):
# #     yt = pytube.YouTube(url)
# #     yt_id = yt.video_id
# #     yt.streams.filter(progressive=True, file_extension='mp4').order_by(
# #         'resolution').desc().first().download(output_path=VIDEOS_PATH, filename=yt_id)
# #     return {"title": yt.title, "id": yt_id, "status": "completed"}

# # def extract_audio_task(yt_id):
# #     audio_extract = extract_audio(yt_id)
# #     print(f" {audio_extract}, {yt_id}")
# #     return audio_extract, yt_id

# # def transcribe_task(args, dest='en'):
# #     audio_extract, yt_id = args
# #     language, segments = transcribe(audio_extract, dest)
# #     serializable_segments = []
# #     for segment in segments:
# #         serializable_segments.append({
# #             'start': segment.start,
# #             'end': segment.end,
# #             'text': segment.text
# #         })
# #     print( f"{language}, {serializable_segments}, {yt_id}")
# #     return language, serializable_segments, yt_id

# # def generate_subtitle_file_task(args):
# #     language, segments_data, yt_id = args
# #     subtitle_file = generate_subtitle_file(yt_id, language, segments_data)
# #     print( f"{audio_extract}, {yt_id}")
# #     return subtitle_file, language, yt_id

# # def add_subtitle_to_video_task(args):
# #     subtitle_file, language, yt_id = args
# #     add_subtitle_to_video(yt_id, subtitle_file, language)
# #     print( f"Subtitle for {yt_id} added")
# #     return f"Subtitle for {yt_id} added"


# # @app.post("/download/")
# # async def download_video_via_url(item: Item):
# #     # Đẩy tác vụ tải video vào hàng đợi Celery
# #     download_video(item.url)
# #     return {"message": "Video download task added to the queue"}


# # @app.post("/generate/{yt_id}")
# # async def generate_subtitle(yt_id: str, dest: str):
# #     task_chain = chain(
# #         extract_audio_task.s(yt_id),
# #         transcribe_task.s(dest),
# #         generate_subtitle_file_task.s(),
# #         add_subtitle_to_video_task.s()
# #     )
    
# #     result = task_chain.delay()
#     # extract_audio_task.s(yt_id)
#     # transcribe_task.s(dest)
#     # generate_subtitle_file_task.s()
#     # add_subtitle_to_video_task.s()
# def download_video(url):
#     yt = pytube.YouTube(url)
#     yt_id = yt.video_id
#     yt.streams.filter(progressive=True, file_extension='mp4').order_by(
#         'resolution').desc().first().download(output_path=VIDEOS_PATH, filename=yt_id)
#     return {"title": yt.title, "id": yt_id, "status": "completed"}

# def extract_audio_task(yt_id):
#     audio_extract = extract_audio(yt_id)
#     print(f" {audio_extract}, {yt_id}")
#     return audio_extract, yt_id

# def transcribe_task(audio_extract, yt_id, dest: str):
#     # audio_extract, yt_id = args
#     language, segments = transcribe(audio_extract, dest)
#     # serializable_segments = []
#     # for segment in segments:
#     #     serializable_segments.append({
#     #         'start': segment.start,
#     #         'end': segment.end,
#     #         'text': segment.text
#     #     })
#     print( f"{language}, {segments}, {yt_id}")
#     return language, segments, yt_id

# def generate_subtitle_file_task(language, segments_data, yt_id):
#     # language, segments_data, yt_id = args
#     subtitle_file = generate_subtitle_file(yt_id, language, segments_data)
#     print( f"{subtitle_file}, {language}, {yt_id}")
#     return subtitle_file, language, yt_id

# def add_subtitle_to_video_task(subtitle_file, language, yt_id):
#     # subtitle_file, language, yt_id = args
#     add_subtitle_to_video(yt_id, subtitle_file, language)
#     print( f"Subtitle for {yt_id} added")
#     return f"Subtitle for {yt_id} added"

# segments = [
#     {"start": 0, "end": 5, "text": "こんにちは"},
#     {"start": 6, "end": 10, "text": "お元気ですか？"}
# ]

# generate_subtitle_file("test_video", "ja", segments)
# @app.post("/download/")
# async def download_video_via_url(item: Item):
#     # Đẩy tác vụ tải video vào hàng đợi Celery
#     download_video(item.url)
#     return {"message": "Video download task added to the queue"}


# @app.post("/generate/{yt_id}")
# async def generate_subtitle(yt_id: str, dest: str):
#     # task_chain = chain(
#     #     extract_audio_task.s(yt_id),
#     #     transcribe_task.s(dest),
#     #     generate_subtitle_file_task.s(),
#     #     add_subtitle_to_video_task.s()
#     # )
    
#     # result = task_chain.delay()
#     audio_extract, yt_id = extract_audio_task(yt_id)
#     language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id, dest)
#     subtitle_file, language, yt_id = generate_subtitle_file_task(language, serializable_segments, yt_id)
#     result = add_subtitle_to_video_task(subtitle_file, language, yt_id)
 
#     print ("message Subtitle task added to the queue")
#     return {"message": "Subtitle task added to the queue"}


# @app.get("/task-status/{task_id}")
# async def task_status(task_id: str):
#     # Kiểm tra trạng thái tác vụ
#     task_result = AsyncResult(task_id)
#     return {"status": task_result.status, "result": task_result.result}


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=Config.FASTAPI_PORT, host=Config.HOST)
import os
import uvicorn
from fastapi import FastAPI
from celery.result import AsyncResult
from src.models.models import Item
from src.utils.utils import *
from src.constant import *
from tasks import download_video, extract_audio_task, transcribe_task, generate_subtitle_file_task, add_subtitle_to_video_task
from config import Config


from src.constant import VIDEOS_PATH


# Create necessary directories
os.makedirs(AUDIOS_PATH, exist_ok=True)
os.makedirs(VIDEOS_PATH, exist_ok=True)
os.makedirs(SUBTITLES, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

app = FastAPI()

@app.post("/download/")
async def download_video_via_url(item: Item):
    # Đẩy tác vụ tải video vào hàng đợi Celery
    download_video(item.url)
    return {"message": "Video download task added to the queue"}


@app.post("/generate/{yt_id}")
async def generate_subtitle(yt_id: str, dest: str):

    audio_extract, yt_id = extract_audio_task(yt_id)
    language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id,dest)
    subtitle_file, language, yt_id = generate_subtitle_file_task(language, serializable_segments, yt_id)
    result = add_subtitle_to_video_task(subtitle_file, dest, yt_id)
 
    print ("message Subtitle task added to the queue")
    return {"message": "Subtitle task added to the queue"}


@app.get("/task-status/{task_id}")
async def task_status(task_id: str):
    # Kiểm tra trạng thái tác vụ
    task_result = AsyncResult(task_id)
    return {"status": task_result.status, "result": task_result.result}


if __name__ == "__main__":
    uvicorn.run("main:app", port=Config.FASTAPI_PORT, host=Config.HOST)