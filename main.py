import os
import uvicorn
from fastapi import FastAPI
from src.models.models import Item
from src.utils.utils import *
from src.constant import *
from tasks import download_video, extract_audio_task, transcribe_task, generate_subtitle_file_task, add_subtitle_to_video_task
import requests

from src.constant import VIDEOS_PATH


# Create necessary directories
os.makedirs(AUDIOS_PATH, exist_ok=True)
os.makedirs(VIDEOS_PATH, exist_ok=True)
os.makedirs(SUBTITLES, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

app = FastAPI()

@app.post("/send_post/")
async def send_download(url: str, dest: str):
    

    download_video(url,dest)

    return {"message":"Video add sucess"}

# @app.post("/download/")
# async def download_video_via_url(item: Item):
#     # Đẩy tác vụ tải video vào hàng đợi Celery
#     download_video(item.url,item.dest)

#     return {"message": "Video download task added to the queue"}


@app.post("/generate/{yt_id}")
async def generate_subtitle(yt_id: str, dest: str):

    audio_extract, yt_id = extract_audio_task(yt_id)
    language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id,dest)
    subtitle_file, language, yt_id = generate_subtitle_file_task(language, serializable_segments, yt_id)
    result = add_subtitle_to_video_task(subtitle_file, dest, yt_id)
    
    print ("message Subtitle task added to the queue")
    return {"message": "Subtitle task added to the queue","file_path":result}


@app.get("/task-status/{task_id}")
async def task_status(task_id: str):
    # Kiểm tra trạng thái tác vụ
    task_result = AsyncResult(task_id)
    return {"status": task_result.status, "result": task_result.result}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)