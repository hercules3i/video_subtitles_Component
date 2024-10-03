from pytube import YouTube

file = YouTube('https://www.youtube.com/watch?v=W10RXr9c44Y')
list_resolution = []
def get_resolution(s):
    list_resolution.append(s.resolution[:-1])
    return int(s.resolution[:-1])
stream = max(
    filter(lambda s: get_resolution(s) <= 1080, 
           filter(lambda s: s.type == 'video', file.fmt_streams)),
    key=get_resolution 
)
stream.download('file.mp4')


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


# list_resolution = []
# def get_resolution(s):
#     list_resolution.append(s.resolution[:-1])
#     return int(s.resolution[:-1])



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

# def download_video_stream(file, selected_resolution):
#     # Tìm luồng video có độ phân giải chính xác với độ phân giải đã chọn
#     stream = next(
#         (s for s in filter(lambda s: s.type == 'video', file.fmt_streams) 
#          if get_resolution(s) == selected_resolution), 
#         None
#     )
    
#     if stream:
#         stream.download('file.mp4')
#         print(f"Đã tải xuống luồng video với độ phân giải {selected_resolution}p.")
#     else:
#         print(f"Không tìm thấy luồng video với độ phân giải {selected_resolution}p.")

# # Ví dụ sử dụng
# selected_resolution =   # Thay đổi độ phân giải theo mong muốn
# download_video_stream(file, selected_resolution)
