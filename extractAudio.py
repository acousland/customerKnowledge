from pydub import AudioSegment
import os

def extractAudio(source, destination):
    if not os.path.isfile(destination):
        print("Extracting audio")
        video = AudioSegment.from_file(source, "mp4")
        video.export(destination, format="mp3")

