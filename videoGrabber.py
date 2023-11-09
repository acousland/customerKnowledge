from pytube import YouTube
#YouTube('https://www.youtube.com/watch?v=zTXi1zFbwpc').streams.first().download()
yt = YouTube('https://www.youtube.com/watch?v=FKbu6YDqQP8')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()