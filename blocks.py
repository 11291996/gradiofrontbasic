import gradio as gr 

#using python decorator with blocks 
with gr.Blocks() as demo1:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")

    @greet_btn.click(inputs=name, outputs=output) #decorator 
    def greet(name):
        return "Hello " + name + "!"

demo1.launch()

#in the example above, the decorator modifies the input
#to modify the output, one have to make the gradio object interactive 

output = gr.Textbox(label="Output", interactive=True)

#if gradio object have default value, it must be set interactive to be modified as well 

def welcome(name):
    return f"Welcome to Gradio, {name}!"

with gr.Blocks() as demo2:
    gr.Markdown(
    """
    # Hello World!
    Start typing below to see the output.
    """)
    inp = gr.Textbox(placeholder="What is your name?")
    out = gr.Textbox()
    inp.change(welcome, inp, out) #due to this change function, the change in inp will be reflected in out with welcome function
    #also Video component can use play() and this will be reflected in the output with a given function when the video is played

demo2.launch()

#multiple data flows

#different bottons deal data differently
def increase(num):
    return num + 1

with gr.Blocks() as demo3:
    a = gr.Number(label="a")
    b = gr.Number(label="b")
    atob = gr.Button("a > b")
    btoa = gr.Button("b > a")
    atob.click(increase, a, b)
    btoa.click(increase, b, a)

demo3.launch()

#more complex example
from transformers import pipeline

asr = pipeline("automatic-speech-recognition", "facebook/wav2vec2-base-960h")
classifier = pipeline("text-classification")


def speech_to_text(speech):
    text = asr(speech)["text"]
    return text


def text_to_sentiment(text):
    return classifier(text)[0]["label"]


demo4 = gr.Blocks()

with demo4:
    audio_file = gr.Audio(type="filepath")
    text = gr.Textbox()
    label = gr.Label()

    b1 = gr.Button("Recognize Speech")
    b2 = gr.Button("Classify Sentiment")

    b1.click(speech_to_text, inputs=audio_file, outputs=text)
    b2.click(text_to_sentiment, inputs=text, outputs=label)

demo4.launch()

#multiple inputs
#also shown in the quickstart.py and reactive_interface.py

with gr.Blocks() as demo5:
    a = gr.Number(label="a")
    b = gr.Number(label="b")
    with gr.Row():
        add_btn = gr.Button("Add")
        sub_btn = gr.Button("Subtract")
    c = gr.Number(label="sum")

    def add(num1, num2):
        return num1 + num2
    add_btn.click(add, inputs=[a, b], outputs=c) #use a list or set to pass multiple inputs

    def sub(data):
        return data[a] - data[b]
    sub_btn.click(sub, inputs={a, b}, outputs=c)

demo5.launch()

#multiple outputs
#also shown in the quickstart.py
#function must return a iterable 
with gr.Blocks() as demo6:
    food_box = gr.Number(value=10, label="Food Count")
    status_box = gr.Textbox()
    def eat(food):
        if food > 0:
            return food - 1, "full"
        else:
            return 0, "hungry"
    gr.Button("EAT").click(
        fn=eat,
        inputs=food_box,
        outputs=[food_box, status_box] #must be a list or set
    )

#function can also return a dictionary
with gr.Blocks() as demo7:
    food_box = gr.Number(value=10, label="Food Count")
    status_box = gr.Textbox()
    def eat(food):
        if food > 0:
            return {food_box: food - 1, status_box: "full"}
        else:
            return {status_box: "hungry"}
    gr.Button("EAT").click(
        fn=eat,
        inputs=food_box,
        outputs=[food_box, status_box]
    )

#configuring the block components
    
def change_textbox(choice):
    if choice == "short":
        return gr.Textbox(lines=2, visible=True)
    elif choice == "long":
        return gr.Textbox(lines=8, visible=True, value="Lorem ipsum dolor sit amet")
    else:
        return gr.Textbox(visible=False) #block configuration has changed


with gr.Blocks() as demo8:
    radio = gr.Radio(
        ["short", "long", "none"], label="What kind of essay would you like to write?"
    )
    text = gr.Textbox(lines=2, interactive=True, show_copy_button=True)
    radio.change(fn=change_textbox, inputs=radio, outputs=text)


demo8.launch()

#using examples with blocks
#shown in reactive_interface.py
def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2


with gr.Blocks() as demo9:
    with gr.Row():
        with gr.Column():
            num_1 = gr.Number(value=4)
            operation = gr.Radio(["add", "subtract", "multiply", "divide"])
            num_2 = gr.Number(value=0)
            submit_btn = gr.Button(value="Calculate")
        with gr.Column():
            result = gr.Number()

    submit_btn.click(calculator, inputs=[num_1, operation, num_2], outputs=[result], api_name=False)
    examples = gr.Examples(examples=[[5, "add", 3],
                                     [4, "divide", 2],
                                     [-4, "multiply", 2.5],
                                     [0, "subtract", 1.2]],
                           inputs=[num_1, operation, num_2])

demo9.launch(show_api=False)

#consecutive events with blocks 
#just like the example in interface_state.py in gradiobackendbasic

import random
import time

with gr.Blocks() as demo10:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        time.sleep(2)
        history[-1][1] = bot_message
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)
    
demo10.queue()
demo10.launch()

#continuous events with blocks
#use configuration every
import plotly.express as px
import numpy as np
import math

plot_end = 2 * math.pi

def get_plot(period=1):
    global plot_end
    x = np.arange(plot_end - 2 * math.pi, plot_end, 0.02)
    y = np.sin(2*math.pi*period * x)
    fig = px.line(x=x, y=y)
    plot_end += 2 * math.pi
    if plot_end > 1000:
        plot_end = 2 * math.pi
    return fig


with gr.Blocks() as demo11:
    with gr.Row():
        with gr.Column():
            gr.Markdown("Change the value of the slider to automatically update the plot")
            period = gr.Slider(label="Period of plot", value=1, minimum=0, maximum=10, step=1)
            plot = gr.Plot(label="Plot (updates every half second)")

    dep = demo11.load(get_plot, None, plot, every=1) #every is the time interval in seconds
    period.change(get_plot, period, plot, every=1, cancels=[dep])

demo11.queue().launch()

