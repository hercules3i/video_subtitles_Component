import moviepy.editor as mpe
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import concurrent.futures

def threadTrim(path_original_vid, video_name, countVid, start: int, end: int):
        new_directory = f"media/short_clip/{video_name}"
        os.makedirs(new_directory, exist_ok=True)

        # Đường dẫn lưu clip
        pathVid = f"{new_directory}/short-{video_name}-{countVid}.mp4"
        
        # Cắt đoạn video
        ffmpeg_extract_subclip(path_original_vid, start, end, targetname=pathVid)
        
        return pathVid

def trimVideo(video_name: str):
    try:
        path_original_vid = f"media/videos/{video_name}"
        video = mpe.VideoFileClip(path_original_vid)
        duration = video.duration

        # the length of video (seconds)
        durationClipVideo = 300

        startTime = -durationClipVideo
        endTime = 0

        listThreads = list()
        countVid = 1
        listPathVid = list()
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            while endTime < duration:
                startTime += durationClipVideo
                endTime += durationClipVideo

                if duration - endTime < durationClipVideo:
                    endTime = duration

                thread = executor.submit(threadTrim,path_original_vid,video_name,countVid,startTime,endTime)
                countVid += 1
                listThreads.append(thread)
        for thread in concurrent.futures.as_completed(listThreads):
            listPathVid.append(thread.result())

        return listPathVid

    except  Exception as e:
        print(e.args)
        
