# example of invoking a function
# NOTE: this example is not robust, 
# sometimes chatgpt will not invoke the tool or not give a text response. Such is life.

import json
from openai import OpenAI
from dotenv import load_dotenv

GPT_MODEL = "gpt-3.5-turbo-0613"
load_dotenv()
client = OpenAI()

# example functions for chatgpt to indirectly invoke using tool calls
def raiseRightArm(): 
    print("*Raising Right Arm*")
    
def raiseLeftArm():
    print("*Raising Left Arm*")

# send messages to chatgpt for response
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

# functions chatgpt can invoke indirectly
tools = [
    {
        "type": "function",
        "function": {
            "name": "raise_right_arm",
            "description": "Raise your right arm",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "raise_left_arm",
            "description": "Raise your left arm",
        }
    }
]

# example to prompt chatgpt to talk while invoking a function
messages = []
messages.append({"role": "system", "content": "If you are asked to perform an action like raising an arm, make sure to always respond to any other user inquiries first."})
messages.append({"role": "user", "content": "Could you tell me a fun fact about lemons while raising your right arm?"})
chat_response = chat_completion_request(
    messages, tools=tools
)
assistant_message = chat_response.choices[0].message
print(assistant_message)

# manually invoke functions chatgpt signalled to invoke
# chatgpt will only ever invoke one function (tool) under our circumstances
if assistant_message.tool_calls is not None:
    call = assistant_message.tool_calls[0]
    
    if call.function.name == "raise_right_arm":
        raiseRightArm()
    elif call.function.name == "raise_left_arm":
        raiseLeftArm()
    else:
        print(f"invalid tool function invokation: {call.function.name}")
        
    assistant_message.content = str(call.function)
    messages.append({"role": assistant_message.role, "content": assistant_message.content})
else:
    messages.append(assistant_message)
    
print("-------------")
print(messages)

messages.append({"role": "user", "content": "Could you tell me a fun fact about oranges?"})
chat_response = chat_completion_request(
    messages, tools=tools
)
assistant_message = chat_response.choices[0].message
print(assistant_message.content)

# manually invoke functions chatgpt signalled to invoke
# chatgpt will only ever invoke one function (tool) under our circumstances
if assistant_message.tool_calls is not None:
    call = assistant_message.tool_calls[0]
    
    if call.function.name == "raise_right_arm":
        raiseRightArm()
    elif call.function.name == "raise_left_arm":
        raiseLeftArm()
    else:
        print(f"invalid tool function invokation: {call.function.name}")
        
    assistant_message.content = str(call.function)
    messages.append({"role": assistant_message.role, "content": assistant_message.content})
else:
    messages.append(assistant_message)