#basic examples of gradio
import gradio as gr

#most simple text interface
def greet(name):
    return "Hello " + name + "!"

demo1 = gr.Interface(fn=greet, inputs="text", outputs="text")

#changing the interface
#placeholder is the text that appears in the input box
demo2 = gr.Interface(fn=greet, inputs=gr.Textbox(lines = 2, placeholder = "Name Here..."), outputs="text") 

#multiple inputs and outputs
def greet_temp(name, is_morning, temperature): #this will be the input list below
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    report = "That's " + str(round(celsius, 2)) + " degrees Celsius"
    return greeting, report

demo3 = gr.Interface(
    fn=greet_temp,
    #checkboxes are used for boolean values
    inputs=["text", "checkbox", gr.Slider(0, 100)], #gets input interfaces as a list
    #slider shows range
    outputs=["text", "text"]
)

#image inputs and outputs
import numpy as np

def sepia(input_img): #changes the rgb values of the image
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img
#automatically uses PIL to convert image to numpy array and apply sepia filter
demo4 = gr.Interface(sepia, gr.Image(), "image") 

#chatbot demo 
import random
#creating a function with message and history parameters
def random_response(message, history): 
    return random.choice(["Yes", "No"])

demo5 = gr.ChatInterface(random_response)

#creating blocks, enables more customization

with gr.Blocks() as demo6: #creates blocks called demo6
    name = gr.Textbox(label="Name") #label is the text that appears above the input box
    output = gr.Textbox(label="Greeting")
    greet_btn = gr.Button("Greet")
    #when the button is clicked, it will call the greet function
    greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet") #also stored as an api 
    #all api can be checked in api page under gradio ui

#more applications 

#define utility functions
def flip_text(x): 
    return x[::-1]


def flip_image(x):
    return np.fliplr(x)

#creating the interface

with gr.Blocks() as demo7:
    gr.Markdown("Flip text or image files using this demo.") #writes a text
    with gr.Tab("Flip Text"): #creates a tab
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")
    with gr.Tab("Flip Image"):
        with gr.Row(): #puts elements below as a row
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

    with gr.Accordion("Open for More!"): #toggle list that hides content until clicked
        gr.Markdown("Look at me...")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

if __name__ == "__main__":
    #to launch the interface, use "gradio app.py" in the terminal
    demo7.launch()