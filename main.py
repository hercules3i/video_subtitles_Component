import os
import uvicorn
from fastapi import FastAPI
from src.models.models import Item
from src.utils.utils import *
from src.constant import *
from tasks import download_video, extract_audio_task, transcribe_task, generate_subtitle_file_task, add_subtitle_to_video_task
import requests
from fastapi.middleware.cors import CORSMiddleware
import shutil

from src.constant import VIDEOS_PATH


# Create necessary directories

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

def remove_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)
        print(f"Thư mục '{directory}' đã được xóa.")
    else:
        print(f"Thư mục '{directory}' không tồn tại.")

# Ví dụ sử dụng

@app.post("/send_post/")
async def send_download(url: str, dest: str):
    os.makedirs(AUDIOS_PATH, exist_ok=True)
    os.makedirs(VIDEOS_PATH, exist_ok=True)
    os.makedirs(SUBTITLES, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)

    download_response = download_video(url,dest)
    yt_id = download_response["id"]
    audio_extract, yt_id = extract_audio_task(yt_id)
    language,video_language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id,dest)
    subtitle_file, language, yt_id, video_content= generate_subtitle_file_task(language,video_language, serializable_segments, yt_id)
    result = add_subtitle_to_video_task(subtitle_file, dest, yt_id)
    print ("message Subtitle task added to the queue")
    remove_directory("media")
    return {"result":result,"videoContent":video_content}

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
    return result


@app.get("/task-status/{task_id}")
async def task_status(task_id: str):
    # Kiểm tra trạng thái tác vụ
    task_result = AsyncResult(task_id)
    return {"status": task_result.status, "result": task_result.result}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)