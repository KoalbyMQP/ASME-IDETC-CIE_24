import speech_recognition as sr
 
# Initialize the recognizer 
r = sr.Recognizer() 

with sr.Microphone() as src:

    # wait to adjust
    print("Adjusting for ambient noise...")
    r.adjust_for_ambient_noise(src, duration=0.2)

    print("Listening for speech")
    #listens for the user's input 
    audio2 = r.listen(src)

    print("Converting to text...")
    # Using google to recognize audio
    txt = r.recognize_google(audio2)

    print(txt)