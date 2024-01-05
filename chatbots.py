import time
import gradio as gr

def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.3)
        yield "You typed: " + message[: i+1] #using yield to use streaming fashion

gr.ChatInterface(slow_echo).launch() 

#additional arguments for gradio chatbot 
def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

gr.ChatInterface(
    yes_man,
    chatbot=gr.Chatbot(height=300), #adjust the chatbot interface 
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7), #adjust the textbox interface
    title="Yes Man",
    description="Ask Yes Man any question",
    theme="soft", #css is also possible 
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    retry_btn=None, #submit, clear, and undo button are available
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch()

#additional inputs 

def echo(message, history, system_prompt, tokens):
    response = f"System prompt: {system_prompt}\n Message: {message}."
    for i in range(min(len(response), int(tokens))):
        time.sleep(0.05)
        yield response[: i+1]
#adding inputs to the chatbot function
gr.ChatInterface(echo, 
                    additional_inputs=[
                        gr.Textbox("You are helpful AI.", label="System Prompt"), 
                        gr.Slider(10, 100)
                    ]
                    ).queue().launch()

#adjusting the chatbot interface as a block 
with gr.Blocks() as demo:
    system_prompt = gr.Textbox("You are helpful AI.", label="System Prompt")
    slider = gr.Slider(10, 100, render=False) #this will be under the chatbot interface

    gr.ChatInterface(
        echo, additional_inputs=[system_prompt, slider]
    )

#one can use the chatbot interface as an api with api_name = chat or gradio_address/chat
    
#using blocks
import random

with gr.Blocks() as demo2:
    chatbot = gr.Chatbot()  
    msg = gr.Textbox() #textbox under the chatbot interface will be created
    clear = gr.ClearButton([msg, chatbot]) #automatically clears the chatbot interface

    def respond(message, chat_history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot]) #submit button will link the function to the chatbot interface

demo2.launch()

#if one changes bot function return to yeild, then it will be a streaming fashion

#using like and dislike buttons
def greet(history, input):
    return history + [(input, "Hello, " + input)]

def vote(data: gr.LikeData): #gr.LikeData will add like and dislike information
    if data.liked:
        print("You upvoted this response: " + data.value)
    else:
        print("You downvoted this response: " + data.value)
    

with gr.Blocks() as demo3:
    chatbot = gr.Chatbot()
    textbox = gr.Textbox()
    textbox.submit(greet, [chatbot, textbox], [chatbot])
    chatbot.like(vote, None, None)  #adding this line causes the like/dislike icons to appear in your chatbot
    
demo3.launch()

#multimodal chatbot
import os

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def add_file(history, file): #defining file adding function
    history = history + [((file.name,), None)]
    return history


def bot(history): #chatbot may return a markdown 
    response = "**That's cool!**"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    ) #adding file to the chatbot interface

    chatbot.like(print_like_dislike, None, None)

demo4.queue()
demo4.launch()

