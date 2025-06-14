#import libraries and dependencies
import pygame #for gui and audio visualization
import sounddevice as sd #for audio input
import numpy as np #for numerical operations
import threading #for multithreading, which is when we handle the audio and gui at the same time
import time #waiting time before moving on to different functions, and other time-related functions
from collections import deque #for storing audio data in a queue-like structure
import sys #for system-specific parameters and functions
import os #for interacting with the operating system to deal with file paths for the agents
import pyttsx3 #text to speech engine for reading out questions and responses
import traceback #for printing stack traces in case of errors
import math #for mathematical operations that make the gui
import pyaudio #for audio recording
import wave #for saving audio files in .wav format
from audio_text_agent import Audio_to_Text_Agent #audio to text agent
from translation_agent import TranslationAgent #translation agent
from llm_agent import LLMAgents #generative and empathy agents

engine = pyttsx3.init() #initialize the text-to-speech engine

#list of questions for homelessness assessments
questions = [
    "What is your name?",
    "How old are you?",
    "Where did you sleep last night?",
    "Have you ever slept in an emergency shelter, safe haven, or transitional housing project?",
    "Have you ever slept in an institution (including hospital, jail, prison, juvenile detention facility, long-term care facility, or nursing home)?",
    "Have you slept in a place not meant for human habitation (including in a car, unsheltered on the street or under a bridge, etc.)?",
    "Have you slept in housing you shared with others, but did not own? If yes, could you continue to stay there – permanently or temporarily?",
    "Have you slept in housing you rented? If yes, did you have a subsidy?",
    "Is there violence or conflict in the place you were staying last night? If yes, do you have another place to go and how long could you potentially stay there?",
    "Is your health or safety at risk in the place you were staying last night (due to situations other than violence, such as substandard housing or severe overcrowding)? If yes, do you have another safe place to go and how long could you potentially stay there?",
    "How long have you stayed in the place you stayed last night?", 
    "Where were you staying prior to the place you stayed last night?", 
    "Do you have any relatives, friends, or acquaintances we should be aware of? How can we contact them?",
    "Do you have a high school diploma or GED?",
    "Have you ever been in foster care?",
    "Have you ever been in the military?",
    "Have you ever been in a mental health facility?",
    "Have you ever been in a substance abuse treatment program?",
    "Have you ever been in a domestic violence shelter?"
]

CHUNK = 1024 #size of audio buffer
FORMAT = pyaudio.paInt16 #format of audio data
CHANNELS = 1 #number of audio channels (1 for mono, 2 for stereo)
RATE = 44100 #sampling rate of audio data
SPEECH_THRESHOLD = 1.0 #volume threshold required to start recording
SILENCE_TIMEOUT = 5  #amount of time audio is less than 1 before recording stops

#this function calculates the volume of the audio data
def get_volume(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.linalg.norm(audio_data) / len(audio_data)

#this function makes a unique filename for each question
def get_next_filename(base="q", ext="wav"):
    n = 1
    while os.path.exists(f"{base}{n}.{ext}"):
        n += 1
    return f"{base}{n}.{ext}", n

#list begins with index 0
n = 0

#this function is how we get the next question in our questions list
def get_next_question():
    global n
    if n >= len(questions):
        print("All questions asked. Exiting.")
        pygame.quit()
        sys.exit()
    n += 1
    return n, questions[n-1]

#this function records audio while the user is talking, and saves it to a file
def record_while_talking():
    filename, q_num = get_next_filename()
    q_num, question = get_next_question()

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    if question == questions[0]:
        introduction = "Hi! I am MiRA. I will just be asking you some questions to get to know you better."
        print(f"Waiting to record answer for question {q_num}...")
        print(f"Question: {question}")
        engine.say(introduction)
        engine.say(question)
        engine.runAndWait()
        
    frames = []
    recording = False
    silence_start = None

    try:
        while True:
            data = stream.read(CHUNK)
            vol = get_volume(data)
            time.sleep(0.005) 

            #if the volume is above 1, we start recording
            if vol >= SPEECH_THRESHOLD:
                if not recording:
                    print(f"Recording answer to q{q_num}...")
                    recording = True
                frames.append(data)
                silence_start = None
            #when volume swictches to below 1 again, we wait for 5 seconds before stopping the recording
            else:
                if recording:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > SILENCE_TIMEOUT:
                        print(f"Finished recording q{q_num}.")
                        break
    except KeyboardInterrupt:
        print("Recording interrupted.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    if frames:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Saved as '{filename}'")
    else:
        print("No audio recorded.")
        
    transcribed_text = Audio_to_Text_Agent(filename).transcribe_to_text(filename) #transcribe audio to text
    language_text = TranslationAgent(transcribed_text).detect_language(transcribed_text) #detect the language of the transcribed text
    translated_text = TranslationAgent(transcribed_text).translate_text(transcribed_text, target_language="en", current_language=language_text) #translate the transcribed text to English if it is not already in English
    
    #generate a response to question user answered, and follow up with the next question
    MiRA_response = LLMAgents(translated_text, questions[n-1], questions[n]).response_agent(
        translated_text, questions[n-1], questions[n]
    )
    
    #make MiRA response sound nicer
    MiRA_empathetic_response = LLMAgents(translated_text, questions[n-1], questions[n]).empathy_agent(MiRA_response)
    engine.say(MiRA_empathetic_response)
    
    #say the response!
    engine.runAndWait()

SAMPLERATE       = 44100 #sampling rate for audio input
BLOCKSIZE        = 1024 #size of audio blocks to process
CHANNELS         = 1 #number of audio channels (1 for mono, 2 for stereo)
VOLUME_THRESHOLD = 0.15 #volume threshold to trigger ripple effect
MIN_RADIUS       = 80 #minimum radius of the ripple effect
MAX_RADIUS       = 120 #maximum radius of the ripple effect
PULSE_SPEED      = 2.0 #speed of the pulse effect
GRADIENT_STEPS   = 100 #number of steps in the gradient circle


#colors of the circle in the gui (it reminds me of cotton candy (yummm!))
BLUE_WC   = (30, 144, 255, 150)
PURPLE    = (138, 43, 226)
PINK      = (255, 105, 180)

volume_level = 0.0 #initially at 0
waveform     = deque(maxlen=BLOCKSIZE) #deque to store audio waveform data
ripples      = [] #list to store ripple effects
stream       = None

#used to analyze new audio data from the microphone
def audio_callback(indata, frames, time, status):
    global volume_level, waveform
    audio = indata[:,0]
    volume_level = np.linalg.norm(audio) * 10
    waveform.extend(audio)

#this function starts the audio stream and sets up the callback to process audio data
def start_audio_stream():
    global stream
    try:
        stream = sd.InputStream(
            callback   = audio_callback,
            channels   = CHANNELS,
            samplerate = SAMPLERATE,
            blocksize  = BLOCKSIZE
        )
        stream.start()
    except Exception:
        traceback.print_exc()
        sys.exit(1)

#make our gradient circle for the gui
def make_gradient_circle(diameter, inner_color, outer_color):
    surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    center = diameter // 2
    for i in range(GRADIENT_STEPS):
        radius = int(center * (1 - i/GRADIENT_STEPS))
        t = i / GRADIENT_STEPS
        r = inner_color[0]*(1-t) + outer_color[0]*t
        g = inner_color[1]*(1-t) + outer_color[1]*t
        b = inner_color[2]*(1-t) + outer_color[2]*t
        a = inner_color[3]*(1-t) + outer_color[3]*t
        pygame.draw.circle(surf, (int(r),int(g),int(b),int(a)), (center,center), radius)
    return surf

#this function fully runs the gui in pygame, and handles user interation to a degree
def run_gui():
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.SRCALPHA)
    pygame.display.set_caption("MiRA Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    base_grad = make_gradient_circle(
        diameter=MAX_RADIUS*2,
        inner_color=BLUE_WC,
        outer_color=(BLUE_WC[0], BLUE_WC[1], BLUE_WC[2], 0)
    )

    t0 = pygame.time.get_ticks() / 1000.0

    running = True
    while running:
        now = pygame.time.get_ticks() / 1000.0
        dt  = now - t0
        t0  = now

        screen.fill((20, 20, 30))

        pulse = (math.sin(2*math.pi*PULSE_SPEED*now) + 1) / 2  # 0→1
        target_rad = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * min(volume_level, 1.0)
        radius = int(MIN_RADIUS + (target_rad - MIN_RADIUS)*pulse)

        grad = pygame.transform.smoothscale(base_grad, (radius*2, radius*2))
        screen.blit(grad, (250-radius, 250-radius), special_flags=pygame.BLEND_PREMULTIPLIED)

        outline_color = PURPLE if volume_level < VOLUME_THRESHOLD else PINK
        pygame.draw.circle(screen, outline_color, (250,250), radius, width=4)

        if volume_level >= VOLUME_THRESHOLD and now - ripple_last[0] > 0.3:
            ripples.append({"r": radius+10, "a":180, "c": outline_color})
            ripple_last[0] = now

        for r in ripples[:]:
            r["r"] += 2
            r["a"] -= 3
            if r["a"] <= 0:
                ripples.remove(r)
                continue
            surf = pygame.Surface((500,500), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (*r["c"], max(0,int(r["a"])) ),
                (250,250),
                int(r["r"]),
                width=2
            )
            screen.blit(surf, (0,0))

        if len(waveform) > 1:
            wf = list(waveform)[::max(1,len(waveform)//180)]
            for i,amp in enumerate(wf):
                angle = (i/len(wf))*2*math.pi
                r1 = radius * 0.6
                r2 = r1 + amp*80
                x1 = 250 + r1*math.cos(angle)
                y1 = 250 + r1*math.sin(angle)
                x2 = 250 + r2*math.cos(angle)
                y2 = 250 + r2*math.sin(angle)
                pygame.draw.line(screen, outline_color, (x1,y1),(x2,y2), 2)

        status = "Listening..." if volume_level < VOLUME_THRESHOLD else "Talking..."
        txt = font.render(status, True, (220,220,220))
        rect = txt.get_rect(center=(250, 450))
        screen.blit(txt, rect)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

#we record the audio while the user is talking
def recording_loop():
    time.sleep(1.0)
    while True:
        record_while_talking()
        time.sleep(0.01)
        
#when the file runs...       
if __name__ == "__main__":
    ripple_last = [0.0]
    print("Starting MiRA…")
    t = threading.Thread(target=start_audio_stream, daemon=True)
    t.start()
    
    rec_thread = threading.Thread(target=recording_loop, daemon=True) #we use a thread to record audio while the gui is running
    rec_thread.start() #start thread
    
    run_gui()
