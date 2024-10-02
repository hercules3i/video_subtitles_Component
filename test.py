from pytube import YouTube

file = YouTube('https://www.youtube.com/watch?v=6aBnhxRvmok')

def get_resolution(s):
    return int(s.resolution[:-1])


stream = max(
    filter(lambda s: get_resolution(s) <= 1080, 
           filter(lambda s: s.type == 'video', file.fmt_streams)),
    key=get_resolution  # maximum resolution among those streams
)
print(stream)
stream.download('file.mp4')