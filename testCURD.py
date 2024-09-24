import requests

class VideoEditor:
    def __init__(self,video_code,video_title, original_video, edited_video):
        self.video_code = video_code,
        self.video_title = video_title,
        self.original_video = original_video
        self.edited_video = edited_video
        
        self.video_content = {}
    
    def save_video_content(self,timeLine,original_language,translated_language):
        time_line = {}
        time_line[timeLine] = {
                "en": original_language,
                "vi": translated_language
        }
        result = {
            "VideoContent": {
                "timeLine": time_line
            }
        }
        self.video_content = result
        return result

    def save(self):
        return {
            "VideoCode": self.video_code ,
            "VideoTitle":self.video_title ,
            "OriginVideoLink":self.original_video,
            "ResultVideoPath":self.edited_video,
            "VideoContent":self.video_content,
            "IsPublic":True,
            "username":"Thai"
        }

import json

# Khởi tạo đối tượng VideoEditor
video_editor = VideoEditor(
    video_code="VID123",
    video_title="Microsoft 365 Copilot Announcement",
    original_video="https://example.com/original_video.mp4",
    edited_video="https://example.com/edited_video.mp4"
)

# Lưu nội dung video
timeLine = "00:00:00,000 --> 00:00:06,800"
original_language = "Today, we are announcing Wave 2 of Microsoft 365 Copilot."
translated_language = "Hôm nay, chúng tôi công bố đợt 2 của Microsoft 365 Copilot."
video_editor.save_video_content(timeLine, original_language, translated_language)

# Lưu toàn bộ thông tin của video
video_data = video_editor.save()

# Lưu dữ liệu vào tệp JSON
with open('save.json', 'w', encoding='utf-8') as json_file:
    json.dump(video_data, json_file, ensure_ascii=False, indent=4)

print("Dữ liệu đã được lưu vào file save.json")
