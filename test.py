from pytube import YouTube

file = YouTube('https://www.youtube.com/watch?v=W10RXr9c44Y')
# list_resolution = []
# def get_resolution(s):
#     list_resolution.append(s.resolution[:-1])
#     return int(s.resolution[:-1])
# stream = max(
#     filter(lambda s: get_resolution(s) <= 1080, 
#            filter(lambda s: s.type == 'video', file.fmt_streams)),
#     key=get_resolution 
# )
# stream.download('file.mp4')


# # res_list = list(list_resolution)

# # # Function to remove duplicates while preserving order
# # def remove_duplicates(res_list):
# #     seen = set()
# #     unique_res = []
# #     for res in res_list:
# #         if res not in seen:
# #             unique_res.append(int(res))
# #             seen.add(res)
# #             unique_resolutions_tuple = tuple(unique_res)

# #     return unique_resolutions_tuple

# # unique_resolutions_tuple = remove_duplicates(res_list)


# # print(unique_resolutions_tuple)


list_resolution = []
def get_resolution(s):
    list_resolution.append(s.resolution[:-1])
    return int(s.resolution[:-1])



# # Function to remove duplicates while preserving order
# def remove_duplicates(res_list):
#     seen = set()
#     unique_res = []
#     for res in res_list:
#         if res not in seen:
#             unique_res.append(int(res))
#             seen.add(res)
#             unique_resolutions_tuple = tuple(unique_res)

#     return unique_res
# def get_resolution(s):
#     list_resolution.append(s.resolution[:-1])
#     return int(s.resolution[:-1])

# def handle_get_resolution(url):
    
#     file = YouTube(url)
#     stream = max(
#     filter(lambda s: get_resolution(s) <= 1080, 
#            filter(lambda s: s.type == 'video', file.fmt_streams)),
#     key=get_resolution 
#     )
    

#     unique_resolutions_tuple = remove_duplicates(list_resolution)
#     return unique_resolutions_tuple

# print(handle_get_resolution("https://www.youtube.com/watch?v=W10RXr9c44Y"))
from pytube import YouTube

def download_video_stream(video_url, selected_resolution):
    # Tạo đối tượng YouTube
    yt = YouTube(video_url)

    # Tìm luồng video và âm thanh với độ phân giải đã chọn
    video_stream = yt.streams.filter(res=selected_resolution, file_extension='mp4', only_video=True).first()
    audio_stream = yt.streams.filter(only_audio=True).first()

    if video_stream and audio_stream:
        # Tải video
        video_file = video_stream.download(filename='video.mp4')
        # Tải âm thanh
        audio_file = audio_stream.download(filename='audio.mp4')
        
        print(f"Đã tải xuống video với độ phân giải {selected_resolution}p.")
        
        # Ghép video và âm thanh lại với nhau
        from moviepy.editor import VideoFileClip, AudioFileClip
        
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)

        # Kết hợp video và âm thanh
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile('file.mp4', codec='libx264')

        # Giải phóng bộ nhớ
        video_clip.close()
        audio_clip.close()
        final_clip.close()
        
        print("Đã kết hợp video và âm thanh thành công.")
    else:
        print(f"Không tìm thấy luồng video hoặc âm thanh với độ phân giải {selected_resolution}p.")

# Ví dụ sử dụng
video_url = 'https://www.youtube.com/watch?v=6aBnhxRvmok'
selected_resolution = '1080p'   
download_video_stream(video_url, selected_resolution)
