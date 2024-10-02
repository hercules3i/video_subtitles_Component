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
import re
from src.constant import VIDEOS_PATH
from pydantic import BaseModel
os.makedirs(AUDIOS_PATH, exist_ok=True)
os.makedirs(VIDEOS_PATH, exist_ok=True)
os.makedirs(SUBTITLES, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)
# Create necessary directories

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
class SubtitleData(BaseModel):
    result: str
    content: list[dict]  # You can further specify the dict structure if neede
def remove_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)
        print(f"Thư mục '{directory}' đã được xóa.")
    else:
        print(f"Thư mục '{directory}' không tồn tại.")

# Ví dụ sử dụng

@app.post("/send_post/")
async def send_download(url: str, dest: str):


    download_response = download_video(url,dest)
    yt_id = download_response["id"]
    audio_extract, yt_id = extract_audio_task(yt_id)
    language, serializable_segments, yt_id = transcribe_task(audio_extract, yt_id,dest)
    # Split the data into blocks based on double newlines


   
    subtitle_file, language, yt_id = generate_subtitle_file_task(language, serializable_segments, yt_id)
    result = add_subtitle_to_video_task(subtitle_file, dest, yt_id)
    print ("message Subtitle task added to the queue")

    return {"result":result, "content":serializable_segments}

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


# Define a Pydantic model for the request body


@app.post("/regenerate")
async def generate_subtitle(subtitle_data: SubtitleData):
    # Access the data from the request body
   
    try:
        result = subtitle_data.result
        content = subtitle_data.content
        print(f"{result}")
        match = re.search(r'output-(.*?)(?:_\w{8})?\.mp4$', result)
        print(f"{match}")
        if match:
            file_id = match.group(1)
            srt_filename = f"{SUBTITLES}sub-{file_id}.srt"
            # Create the SRT file
            
            with open(srt_filename, 'w', encoding='utf-8') as srt_file:
                for index, item in enumerate(content, start=1):
                    start_time = format_time(item['start'])
                    end_time = format_time(item['end'])
                    srt_file.write(f"{index}\n")
                    srt_file.write(f"{start_time} --> {end_time}\n")
                    srt_file.write(f"{item['text']}\n") 
                    srt_file.write(f"{item['translated_text']}\n\n") # Change here to use 'text' instead of 'translated_text'
                first_dash_index = result.index('-') + 1  # +1 to get the position after the first '-'

            last_dash_index = result.rindex('-')  # Get the position of the last '-'

            # Extract videoID (from first '-' to last '-')
            videoID = result[first_dash_index:last_dash_index]

            # Extract the last part before the last '_'
            last_part_before_underscore = result.rsplit('_', 1)[0]  # Get everything before the last '_'
            lang_code_candidate = last_part_before_underscore[-8:]  # Get the last 8 characters

            # Check if the last 8 characters contain any valid language codes
            valid_langs = {"zh-CN", "zh-TW", "mni-Mtei"}
            if lang_code_candidate in valid_langs:
                dest = lang_code_candidate  # If it matches, set dest to this value
            else:
                # Extract the 'dest' (last '-' to the next '_')
                dest_match = re.search(r'-(\w{2,3})_', result)  # Match language codes of at least 2 or 3 characters before '_'
                if dest_match:
                    dest = dest_match.group(1)  # Get the dest
                else:
                    dest = None  # Default to None if no match
            print(f"videoID {videoID} dest {dest}")
        
        
            print(f"SRT file '{srt_filename}' created successfully.")
            url = add_subtitle_to_video_task(srt_filename, dest, videoID)
            return url
        else:
            print("dont have video id")
    except Exception as e:
        return "Error " + e
# Function to format time in SRT format
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"


@app.get("/task-status/{task_id}")
async def task_status(task_id: str):
    # Kiểm tra trạng thái tác vụ
    task_result = AsyncResult(task_id)
    return {"status": task_result.status, "result": task_result.result}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)