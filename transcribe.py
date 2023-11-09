import whisper
import os

def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return(result)

def transcribePersist(audio_path, destination):
    if not os.path.isfile(destination):
        transcription = transcribe(audio_path)
        with open(destination, 'w') as transcript_file:
            transcript_file.write(f"{transcription}\n\n")

def transcribeRead(transcript_path):
    if os.path.isfile(transcript_path):
        with open(transcript_path, 'r') as file:
            call_transcription = file.read()
        return(call_transcription)
    else:
        return("Transcript not found")
