# Have Finley answer one question
# Basic version of TalkToFinleyConverstaion

import os
from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
import pygame
 
r = sr.Recognizer() 

# feed text to openai
load_dotenv()  # take environment variables from .env.
client = OpenAI()

# initialize pygame for TTS
pygame.init()
pygame.mixer.init()

# step 1: listen for question and convert speech to text
with sr.Microphone() as src:

    # wait to adjust
    print("Adjusting for ambient noise...")
    r.adjust_for_ambient_noise(src, duration=0.2)

    print("Listening for speech")
    #listens for the user's input 
    audio2 = r.listen(src)

    print("Converting to text...")
    # Using google to recognize audio
    spokenText = r.recognize_google(audio2)

    print(spokenText)
    
# step 2: feed question to openai
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a humanoid robot named Finley, designed to assist humans with factual questions about U.S. History. Please keep your answers brief, only a few sentences maximum."},
    {"role": "user", "content": spokenText}
  ]
)

print(completion.choices[0].message.content)

# step 3: speak openai's response using TTS

# Uses openai's TTS to generate a sound file and pygame to play back the file
response = client.audio.speech.create(
    model="tts-1",
    voice="fable",
    input=completion.choices[0].message.content,
)

outputFile = "output.mp3"

response.stream_to_file(outputFile)

# play mp3 file
pygame.mixer.music.load(outputFile)
pygame.mixer.music.play()

# wait for playback to end
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == SONG_END:
            done = True

# delete file when done
print("done")
pygame.mixer.music.unload()
os.remove(outputFile) 