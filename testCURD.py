import os
import urllib.parse

def is_local_file(url):
    # Kiểm tra xem URL có phải là file cục bộ không
    parsed_url = urllib.parse.urlparse(url)
    
    # Kiểm tra nếu là file:// hoặc có định dạng đường dẫn cục bộ
    if parsed_url.scheme == "file":
        return True
    elif parsed_url.scheme == "":
        # Xử lý đường dẫn cục bộ (Windows hoặc Unix)
        return os.path.exists(url)
    
    return False

# Ví dụ sử dụng
url1 = "C:/Users/vietnam3i/Downloads/testvideo"
url2 = "file:///C:/Users/vietnam3i/Downloads/testvideo"
url3 = "https://example.com/video.mp4"

print(is_local_file(url1))  # True hoặc False
print(is_local_file(url2))  # True
print(is_local_file(url3))  # False
