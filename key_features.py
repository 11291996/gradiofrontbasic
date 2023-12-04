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
input_img = gr.Image(shape=(100, 100), type="pil") #getting data as PIL 
#post
output_img = gr.Image(invert_colors=True, type="numpy") #returning numpy array

if __name__ == "__main__":
    demo5.launch() #launches the interface