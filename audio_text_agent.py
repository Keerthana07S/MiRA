#import libraries and dependencies
import speech_recognition as sr #will allow us to transcribe audio response to text

#initialize the audio recognizer
recognizer = sr.Recognizer()

#class for converting audio response to text
class Audio_to_Text_Agent:
    def __init__(self, audio_file: str):
        self.audio_file = audio_file #audio file (.wav) to be transcribed
        
    #function to transcribe audio file to text
    def transcribe_to_text(self, audio_file: str):
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        
        #return text
        return recognizer.recognize_google(audio_data)
    
