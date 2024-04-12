import whisper
import os

def transcribe(audio_path, model):
    print("Transcribing")
    model = whisper.load_model(model)
    result = model.transcribe(audio_path)
    return(result["text"])

def transcribePersist(audio_path, destination, model):
    if not os.path.isfile(destination):
        transcription = transcribe(audio_path, model)
        with open(destination, 'w') as transcript_file:
            transcript_file.write(f"{transcription}\n\n")

def transcribeRead(transcript_path):
    if os.path.isfile(transcript_path):
        with open(transcript_path, 'r') as file:
            call_transcription = file.read()
        return(call_transcription)
    else:
        return("Transcript not found")
