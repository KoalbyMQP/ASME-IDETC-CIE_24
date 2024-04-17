# Converse back and forth with Finley, with memory of previous conversation points

import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
from speech_recognition.exceptions import UnknownValueError
import pygame

r = sr.Recognizer() 

# feed text to openai
load_dotenv()  # take environment variables from .env.
client = OpenAI()

# initialize pygame for TTS
pygame.init()
pygame.mixer.init()

# start with context from system and add user queries/assistant responses as they happen
previousMessages = []

def listenForQuestion():
    success = False
    
    while not success:
    # step 1: listen for question and convert speech to text
        try:
            with sr.Microphone() as src:

                # wait to adjust
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(src, duration=0.2)

                print("Listening for speech. Say quit, stop, or exit to stop.")
                # listens for the user's input 
                audio2 = r.listen(src)

                print("Converting to text...")
                # Using google to recognize audio
                spokenText = r.recognize_google(audio2)
                success = True
        except UnknownValueError:
            print("Did not understand speech, try again.")

    return spokenText

# Ask Finley a question and have him speak the response
# inputPrompt: The question to ask Finley
def respondWithSpeech(inputPrompt):
    global previousMessages
    
    # feed question and past conversation history to openai
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "Pretend you are a physical humanoid robot assistant named Finley with arms and legs, designed to assist humans with factual questions about U.S. History. Please keep your answers brief, only a few sentences maximum."},
          {"role": "system", "content": f"Any past conversation history will be listed now:{''.join(previousMessages)}"},
          {"role": "user", "content": inputPrompt},
      ]
    )

    print("\n" + completion.choices[0].message.content + "\n")
    
    # add assistant response to history as context for future interactions
    previousMessages.append(f"User: {inputPrompt}\n")
    previousMessages.append(f"Assistant: {completion.choices[0].message.content}\n")
    
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

# Loop to converse with Finley
def main():
    while True:
        spokenText = listenForQuestion()

        print(spokenText)
            
        if spokenText.lower() in ['quit', 'stop', 'exit']:
            sys.exit(0)

        respondWithSpeech(spokenText)