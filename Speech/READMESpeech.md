# Talk To Finley

Using speech recognition, talk to Finley through a microphone. Finley will process your question and respond using his voice!

## Setup

### Install the latest version of Python 3
- https://www.python.org/downloads/

### Clone this repository
- Using github desktop: https://desktop.github.com/

OR

- Open terminal (mac/linux) or command prompt (windows) in the desired folder
- Download repository with  ```git clone https://github.com/KoalbyMQP/TalkToFinley```

### Install required python packages
- Open terminal (mac/linux) or command prompt (windows) in the repository folder
- Install python modules with ```pip install -r requirements.txt```

### Tell git to ignore changes to .env to avoid publicly leaking openai API key
- In the same folder: ```git update-index --assume-unchanged .env```

### Setup OpenAI API key for response generation and (optionally) TTS
- ask Jatin nicely to use his key :)

OR

- NOTE: you need to insert at least $5 into your account to use the API. Proceed with these steps if you are ok with this.
- Create an OpenAI account: https://openai.com
- Navigate to https://platform.openai.com/api-keys
- Click Create New Secret Key (give it a name, default settings are fine)
- Copy key into .env, replacing 'abc123'
- Go to https://platform.openai.com/account/billing/overview
- Click on 'Payment methods' and add a payment method 
- Add at least $5 worth of credits ($5 will be more than enough)
- (optional) delete payment method and disable auto recharge

## Run Talk to Finley

### Requirements
- Python >= 3
- Microphone
- Speaker

### Run code
- run TalkToFinley.py in IDE, or navigate to repository folder in terminal/command prompt and run ```python TalkToFinley.py```
- Wait for 'Listening for speech' prompt in terminal
- Speak your question
    - The program will automatically stop listening when it hears a long enough pause. 
    - NOTE: ChatGPT does not have access to the internet or information beyond 2021.
- Wait for response to generate and TTS to begin playing.