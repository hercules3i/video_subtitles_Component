from flask import Flask
import concurrent.futures
import time
app = Flask(__name__)

import concurrent.futures
import time
def add_two(number):
    """Cộng 2 vào số đã cho."""
    return number + 2

def subtract_two(number):
    """Trừ 2 từ số đã cho."""
    return number - 2

def multiply_by_two(number):
    """Nhân số đã cho với 2."""
    return number * 2

def divide_by_two(number):
    """Chia số đã cho cho 2."""
    if number == 0:
        return "Cannot divide by zero"
    return number / 2
def task(n):
    
    print(add_two(n))
    print(subtract_two(n))
    print(multiply_by_two(n))
    print(divide_by_two(n))
    
    return f"Task {n} complete"

# Danh sách thời gian ngủ cho các task
durations = [3]

# Tạo một danh sách chứa các Future
listThreads = []

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    for duration in durations:
        future = executor.submit(task, duration)
        listThreads.append(future)
    print(listThreads)
    # Xử lý kết quả ngay khi chúng hoàn thành
    for future in concurrent.futures.as_completed(listThreads):
        print(future.result())  # In ra kết quả
