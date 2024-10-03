from moviepy.editor import VideoFileClip

# Đường dẫn tới video
video_path = 'duong_dan_toi_video.mp4'

# Tải video
video = VideoFileClip(video_path)

# Trích xuất âm thanh
audio = video.audio

# Lưu âm thanh thành file
audio.write_audiofile('duong_dan_toi_am_thanh.mp3')

# Đóng video và âm thanh
video.close()
audio.close()
