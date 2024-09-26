import requests

URL = "https://admin.metalearn.vn/MobileLogin/UploadFile"

def post_to_db(file_path):
    # Mở file ở chế độ đọc nhị phân
    with open(file_path, 'rb') as file:
        files = {'file': file}  # Đặt file vào trong dictionary
        response = requests.post(URL, files=files)

    # Kiểm tra nếu request thành công
    if response.status_code == 200:
        # Chuyển đổi nội dung phản hồi sang JSON
        json_data = response.json()

        # Kiểm tra nếu không có lỗi trong phản hồi
        if not json_data.get('Error', True):
            # Truy cập vào đường dẫn FilePath
            file_path = json_data["Object"]["FilePath"]
            print("Filepath output:", file_path)
            return file_path
        else:
            print("Có lỗi xảy ra:", json_data.get("Title", "Unknown error"))
    else:
        print(f"Lỗi khi upload: {response.status_code}")
        print(response.text)