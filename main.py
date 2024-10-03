import os
import uvicorn
from fastapi import FastAPI
from src.models.models import Item
from src.utils.utils import *
from src.constant import *
from tasks import handle_get_resolution,redownload_video, download_video, extract_audio_task, transcribe_task, generate_subtitle_file_task, add_subtitle_to_video_task
import requests
from fastapi.middleware.cors import CORSMiddleware
import shutil
import re
from src.constant import VIDEOS_PATH
from pydantic import BaseModel

# Create necessary directories
os.makedirs(AUDIOS_PATH, exist_ok=True)
os.makedirs(VIDEOS_PATH, exist_ok=True)
os.makedirs(SUBTITLES, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
class SubtitleData(BaseModel):
    dest : str
    url: str
    content: list[dict]  # You can further specify the dict structure if neede
    res: int

@app.post("/send_post/")
async def send_download(url: str, dest: str, res: int):
   
    # try:
        download_response = download_video(url,res)
        yt_id = download_response["id"]
        audio_extract, yt_id = extract_audio_task(yt_id)
        language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id,dest)
        # Split the data into blocks based on double newlines        
            
        subtitle_file, language, yt_id = generate_subtitle_file_task(language, serializable_segments, yt_id)
        result = add_subtitle_to_video_task(subtitle_file, dest, yt_id)
        print ("message Subtitle task added to the queue")
        os.remove(audio_extract)
        os.remove(subtitle_file)

        os.remove(f"{VIDEOS_PATH}{yt_id}")
        
        return {"result":result, "content":serializable_segments}

# @app.post("/download/")
# async def download_video_via_url(item: Item):
#     # Đẩy tác vụ tải video vào hàng đợi Celery
#     download_video(item.url,item.dest)

#     return {"message": "Video download task added to the queue"}

@app.post("/generate/{yt_id}")
async def generate_subtitle(yt_id: str, dest: str):
    try:
        audio_extract, yt_id = extract_audio_task(yt_id)
        language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id,dest)
        subtitle_file, language, yt_id = generate_subtitle_file_task(language, serializable_segments, yt_id)
        result = add_subtitle_to_video_task(subtitle_file, dest, yt_id)
        
        print ("message Subtitle task added to the queue")
        return result
    except Exception as e:
        return e


# Define a Pydantic model for the request body


@app.post("/regenerate")
async def generate_subtitle(subtitle_data: SubtitleData):
    # Access the data from the request body
 
    try:
        dest = subtitle_data.dest
        url = subtitle_data.url
        content = subtitle_data.content
        res = subtitle_data.res
        print(f"{url}")
        download_response = redownload_video(url,res)
        videoId  = download_response["id"]+'-'+dest
        if videoId:
           
            srt_filename = f"{SUBTITLES}sub-{videoId}.srt"
            # Create the SRT file
            
            with open(srt_filename, 'w', encoding='utf-8') as srt_file:
                for index, item in enumerate(content, start=1):
                    start_time = format_time(item['start'])
                    end_time = format_time(item['end'])
                    srt_file.write(f"{index}\n")
                    srt_file.write(f"{start_time} --> {end_time}\n")
                    srt_file.write(f"{item['text']}\n") 
                    try:
                      srt_file.write(f"{item['translated_text']}\n\n") # Change here to use 'text' instead of 'translated_text'
                    except:
                        continue
            
        
            print(f"SRT file '{srt_filename}' created successfully.")
            url = add_subtitle_to_video_task(srt_filename, dest, "re-"+download_response["id"])
            os.remove(srt_filename)
            os.remove(f"{VIDEOS_PATH}re-{download_response['id']}")

            return url
        else:
            print("dont have video id")
    except Exception as e:
        return e
# Function to format time in SRT format
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

@app.post("/get_video_resolutions/")
async def get_video_resolutions(url: str):
    try:
        list_resolutions,time_length = handle_get_resolution(url)
        return {"list_resolutions": list_resolutions,"time_length":time_length}
    except Exception as e:
        return e

@app.post("/task-status/")
async def task_status():
    
    return {"status": "Hệ thống sẵn sàng"}


