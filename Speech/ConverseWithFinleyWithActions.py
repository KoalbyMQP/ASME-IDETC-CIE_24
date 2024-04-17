# Converse back and forth with Finley, with memory of previous conversation points
# Finley can also perform basic actions (simulated as function calls) when prompted

import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
from speech_recognition.exceptions import UnknownValueError
import pygame

# Tool functions chatgpt can invoke indirectly
def endConversation():
    print("Ending conversation...")
    sys.exit(0)

def raiseLeftArm():
    print("*Raising left arm*")

def raiseRightArm():
    print("*Raising right arm*")

def lowerLeftArm():
    print("*Lowering left arm*")

def lowerRightArm():
    print("*Lowering right arm*")

# Initialization
r = sr.Recognizer()

# feed text to openai
load_dotenv()  # take environment variables from .env.
client = OpenAI()

# initialize pygame for TTS
pygame.init()
pygame.mixer.init()

# start with context from system and add user queries/assistant responses as they happen
previousMessages = []

# Listen for speech through the microphone to convert to a text query for chatgpt
def listenForQuestion():
    success = False

    while not success:
        # step 1: listen for question and convert speech to text
        try:
            with sr.Microphone() as src:

                # wait to adjust
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(src, duration=0.5)

                print("Listening for speech. Say just 'quit', 'stop', or 'exit' to exit from the program.")
                # listens for the user's input
                audio2 = r.listen(src, timeout=10)

                print("Converting to text...")
                # Using google to recognize audio
                spokenText = r.recognize_google(audio2)
                
                success = True
        except UnknownValueError:
            print("Did not understand speech, try again.")

    if spokenText.lower() in ["quit", "stop", "exit"]:
        endConversation()

    return spokenText

# Ask Finley a question and have him speak the response
# inputPrompt: The question to ask Finley
def respondWithSpeech(inputPrompt):
    global previousMessages

    # feed question and past conversation history to openai
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": """
                You must make sure to always respond to any user questions or statements before performing a requested action, such as raising one of your arms.
                Your name is Finley, you are a humanoid robot assistant. Your father is Koalby and your mother is Ava, they are both humanoids created by WPI students. 
                Please keep your answers brief, only a few sentences maximum. 
                Your creators are Merel Sutherland, Wil Michels, Anna McCusker, and Shivank Gupta. The project's advisor is Pradeep Radhakrishnan, Ph.D. 
                Users will be judges in a competition, asking you to perform certain actions and undertand your function.
                
            

            """,
            },
            {"role": "system", "content": f"Any past conversation history will be listed now:{''.join(previousMessages)}",},
            {"role": "system", "content": "Remember, if a user asks you a question and tells you to perform an action, always answer the question first before performing the action. This is very important.",},
            {"role": "user", "content": inputPrompt},
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "endConversation",
                "description": "say goodbye when the user indicates or implies they are done talking to you",
            },
        },{
            "type": "function",
            "function": {
                "name": "raiseLeftArm",
                "description": "Raise your left arm",
            },
        },{
            "type": "function",
            "function": {
                "name": "raiseRightArm",
                "description": "Raise your right arm",
            },
        },{
            "type": "function",
            "function": {
                "name": "lowerLeftArm",
                "description": "Lower your left arm",
            },
        },{
            "type": "function",
            "function": {
                "name": "lowerRightArm",
                "description": "Lower your right arm",
            },
        },],
    )

    assistant_message = completion.choices[0].message
    print(assistant_message)

    # add assistant response to history as context for future interactions
    previousMessages.append(f"User: {inputPrompt}\n")
    previousMessages.append(f"Assistant: {assistant_message.content}\n")

    # manually invoke functions chatgpt signalled to invoke
    # chatgpt will only ever invoke one function (tool) under our circumstances
    if assistant_message.tool_calls is not None:
        call = assistant_message.tool_calls[0]
        
        if call.function.name == "endConversation":
            endConversation()
        elif call.function.name == "raiseLeftArm":
            raiseLeftArm()
        elif call.function.name == "raiseRightArm":
            raiseRightArm()
        elif call.function.name == "lowerLeftArm":
            lowerLeftArm()
        elif call.function.name == "lowerRightArm":
            lowerRightArm()
        else:
            print(f"invalid tool function invokation: {call.function.name}")

    # step 3: speak openai's response using TTS


    if assistant_message.content is not None:
        # Uses openai's TTS to generate a sound file and pygame to play back the file
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable", # change voice here
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

        respondWithSpeech(spokenText)