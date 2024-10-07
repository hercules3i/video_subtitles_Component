# from pytube import YouTube

# file = YouTube('https://www.youtube.com/watch?v=W10RXr9c44Y')


# list_resolution = []
# def get_resolution(s):
#     list_resolution.append(s.resolution[:-1])
#     return int(s.resolution[:-1])

# from pytube import YouTube

# def download_video_stream(video_url, selected_resolution):
#     # Tạo đối tượng YouTube
#     yt = YouTube(video_url)

#     # Tìm luồng video và âm thanh với độ phân giải đã chọn
#     video_stream = yt.streams.filter(res=selected_resolution, file_extension='mp4', only_video=True).first()
#     audio_stream = yt.streams.filter(only_audio=True).first()

#     if video_stream and audio_stream:
#         # Tải video
#         video_file = video_stream.download(filename='video.mp4')
#         # Tải âm thanh
#         audio_file = audio_stream.download(filename='audio.mp4')
        
#         print(f"Đã tải xuống video với độ phân giải {selected_resolution}p.")
        
#         # Ghép video và âm thanh lại với nhau
#         from moviepy.editor import VideoFileClip, AudioFileClip
        
#         video_clip = VideoFileClip(video_file)
#         audio_clip = AudioFileClip(audio_file)

#         # Kết hợp video và âm thanh
#         final_clip = video_clip.set_audio(audio_clip)
#         final_clip.write_videofile('file.mp4', codec='libx264')

#         # Giải phóng bộ nhớ
#         video_clip.close()
#         audio_clip.close()
#         final_clip.close()
        
#         print("Đã kết hợp video và âm thanh thành công.")
#     else:
#         print(f"Không tìm thấy luồng video hoặc âm thanh với độ phân giải {selected_resolution}p.")

# # Ví dụ sử dụng
# video_url = 'https://www.youtube.com/watch?v=6aBnhxRvmok'
# selected_resolution = '1080p'   
# download_video_stream(video_url, selected_resolution)
import yt_dlp

def download_video(url):
    ydl_opts = {
        # 'format': 'bestvideo[height>=360]+bestaudio/best[height>=360]',  # lowest video above or equal to 360p
        'format': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',  # best video/audio up to 1440p
        # 'format': 'bestvideo+bestaudio/best',  # best video and audio available
        'outtmpl': 'downloaded_video.mp4',  # output file template
        'noplaylist': True,  # download only the single video, not the playlist
        'merge_output_format': 'mp4',  # specify the output format to avoid separate files
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(f"Downloaded: {info_dict['title']}")
    except Exception as e:
        print(f"Error downloading video: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=ZrpEIw8IWwk"
download_video(video_url)
