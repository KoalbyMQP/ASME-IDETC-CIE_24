# Uses openai's TTS to generate a sound file and pygame to play back the file

import os
import pygame
from dotenv import load_dotenv
from openai import OpenAI

# generate speech using openai TTS
load_dotenv()  # take environment variables from .env.
client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="The quick brown fox jumps over the lazy dog.",
)

outputFile = "output.mp3"

response.stream_to_file(outputFile)
 
# play mp3 file
pygame.init()
pygame.mixer.init()
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