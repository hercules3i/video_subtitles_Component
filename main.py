
import os
import uvicorn
from fastapi import FastAPI
from src.models.models import Item
from src.utils.utils import *
from src.constant import *
from tasks import download_video, extract_audio_task, transcribe_task, generate_subtitle_file_task, add_subtitle_to_video_task
from trim_video import trimVideo
import concurrent.futures
import time

from src.constant import VIDEOS_PATH


# Create necessary directories
os.makedirs(AUDIOS_PATH, exist_ok=True)
os.makedirs(VIDEOS_PATH, exist_ok=True)
os.makedirs(SUBTITLES, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

app = FastAPI()
from tqdm import tqdm
from multiprocessing import Lock
tqdm.set_lock(Lock())  # manually set internal lock
@app.post("/download/")
async def download_video_via_url(item: Item):
    # Đẩy tác vụ tải video vào hàng đợi Celery
    result = download_video(item.url)
    trimVideo(result["id"])
    return {"message": "Video download task added to the queue"}

def generate(clip_id,dest,yt_id):
    audio_extract, clip_id = extract_audio_task(clip_id,yt_id)
    language, serializable_segments, clip_id = transcribe_task(audio_extract, clip_id,dest,yt_id)
    subtitle_file, language, clip_id = generate_subtitle_file_task(language, serializable_segments, clip_id)
    result = add_subtitle_to_video_task(subtitle_file, dest, clip_id,yt_id)
    return f"{clip_id} edited!!!!!"
def list_files_in_directory(directory_path):
    try:
        # Lấy danh sách tên file trong thư mục
        files = os.listdir(directory_path)
        return files
    except Exception as e:
        return str(e)
@app.post("/generate/{yt_id}")
async def generate_subtitle(yt_id: str, dest: str):
    listThreads = []
    filenames = list_files_in_directory(f"./media/short_clip/{yt_id}/")
    print(filenames)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for video_id in filenames:
            future = executor.submit(generate, video_id,dest,yt_id)
            listThreads.append(future)
        print(listThreads)
        # Xử lý kết quả ngay khi chúng hoàn thành
        for future in concurrent.futures.as_completed(listThreads):
            print(future.result())  # In ra kết quả

 
    print ("message Subtitle task added to the queue")
    return {"message": "Subtitle task added to the queue"}


# @app.get("/task-status/{task_id}")
# async def task_status(task_id: str):
#     # Kiểm tra trạng thái tác vụ
#     task_result = AsyncResult(task_id)
#     return {"status": task_result.status, "result": task_result.result}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
    