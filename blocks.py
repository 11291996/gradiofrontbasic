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

