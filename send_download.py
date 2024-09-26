import requests
from fastapi import FastAPI

app = FastAPI()  # Sử dụng FastAPI thay vì fastapi()

@app.post("/send_post/")
async def send_download(url: str, dest: str):
    # URL cho API khác mà bạn muốn gửi request đến
    URL = "http://127.0.0.1:8002/download/"
    
    # Dữ liệu được gửi trong request POST
    data = {
        "url": url,
        "dest": dest
    }

    # Gửi request POST đến URL và nhận phản hồi
    response = requests.post(URL, json=data)

    # In phản hồi từ server
    print(response.json())

    # Trả về phản hồi
    return {"message": "Request sent", "response_status": response.status_code}
