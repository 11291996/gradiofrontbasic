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
                    )

#adjusting the chatbot interface as a block 
with gr.Blocks() as demo:
    system_prompt = gr.Textbox("You are helpful AI.", label="System Prompt")
    slider = gr.Slider(10, 100, render=False) #this will be under the chatbot interface

    gr.ChatInterface(
        echo, additional_inputs=[system_prompt, slider]
    )

#one can use the chatbot interface as an api with api_name = chat or gradio_address/chat