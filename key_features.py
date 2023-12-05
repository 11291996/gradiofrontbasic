import gradio as gr

#example inputs
#function for the interface
def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise gr.Error("Cannot divide by zero!") #error can be raised via Gradio
        return num1 / num2

demo1 = gr.Interface(
    calculator,
    [
        "number", 
        gr.Radio(["add", "subtract", "multiply", "divide"]), #radio buttons
        "number"
    ],
    "number",
    examples=[ #can make examples for the inputs and the users can also select one of them
        [45, "add", 3],
        [3.14, "divide", 2],
        [144, "multiply", 2.5],
        [0, "subtract", 1.2],
    ],
    title="Toy Calculator", #demo title
    description="Here's a sample toy calculator. Allows you to calculate things like 2+2=4", #demo description like a markdown
)

#alert
def start_process(name):
    gr.Info("Starting process") #can make info box
    if name is "": 
        gr.Warning("Name is empty") #also warning can be raised unlike error it keeps the progress
    return name

demo2 = gr.Interface(start_process, inputs = "text", outputs = "text")

#adding description on interface

demo3 = gr.Interface(start_process, inputs = "text", outputs = "text",
                     title = "Warning Test",
                     description = "this will be under the title",
                     article = "this will be under the interface"
                     )
#with blocks
with gr.Blocks() as demo4:
    #use markdown grammar with this block
    gr.Markdown("""
                # this is from markdown 
                """
                ) 
    gr.HTML("<p>this is from html</p>") #use html grammar with this block
    gr.Number(info = "just put in numbers") #gets int data type #info explains further detail of the input boxes

#flagging
#logs each input and output
demo5 = gr.Interface(start_process, inputs = "text", outputs = "text", flagging_dir = "./demo5_flag") #default is "./flagged"
#flag button will appear as a default and if one clicks it it logs the components of the interface and other meta data

#preprocessing and postprocessing 
#pre
input_img = gr.Image(height = 100, width = 100, type="pil") #getting data as PIL 
#post
output_img = gr.Image(image_mode="I", type="numpy") #returning numpy array

#style
demo6 = gr.Interface(start_process, inputs = "text", outputs = "text", theme = gr.themes.Monochrome())

with gr.Interface(start_process, inputs = "text", outputs = "text", css=".gradio-container {backgroud-color: red}") as demo7: 
    #css can be passed to gradio as well 
    pass #basic class is called gradio-container

#queue 
demo6.queue() #limits the number of requests that are processed at a single time
#this prevents hardware errors

with gr.Blocks() as demo7:
    btn = gr.Button("Run")
    def hi():
        return "hi"
    output = gr.Textbox(label = "output")
    btn.click(hi, None, output)

#iterative output 
#use python yield 
import numpy as np
import time

def fake_diffusion(steps):
    for _ in range(steps):
        time.sleep(1) #show the speed of the iteration
        image = np.random.random((600, 600, 3))
        yield image
    image = np.ones((1000,1000,3), np.uint8)
    image[:] = [255, 124, 0]
    yield image

demo8 = gr.Interface(fake_diffusion, inputs=gr.Slider(1, 10), outputs="image") 
#3rd argument of a slider shows how many digits with the float

#define queue - required for generators
demo8.queue()

#progressive bar

def slowly_reverse(word, progress=gr.Progress()): #creating progress bar
    #if Progress() has track_tqdm=True -> tqdm is tracked if the function uses it
    progress(0, desc="Starting")
    time.sleep(1)
    progress(0.05)
    new_string = ""
    for letter in progress.tqdm(word, desc="Reversing"):
        time.sleep(0.25)
        new_string = letter + new_string
    return new_string

demo9 = gr.Interface(slowly_reverse, gr.Textbox(), gr.Textbox())

if __name__ == "__main__":
    demo9.launch() #launches the interface