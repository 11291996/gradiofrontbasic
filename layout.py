#controling the layout of gradio components 
import gradio as gr 

with gr.Blocks() as demo:
    with gr.Row(equal_height=True): #all components in this row will have equal height
        textbox = gr.Textbox()
        btn2 = gr.Button("Button 2")

#scale orders the portion of the Row or Column that each component takes up
with gr.Blocks() as demo2:
    with gr.Row():
        btn0 = gr.Button("Button 0", scale=0)
        btn1 = gr.Button("Button 1", scale=1)
        btn2 = gr.Button("Button 2", scale=2)

#min_width will set the minimum width of the components

#dropdowns        
with gr.Blocks() as demo3:
    with gr.Row():
        text1 = gr.Textbox(label="t1")
        slider2 = gr.Textbox(label="s2")
        drop3 = gr.Dropdown(["a", "b", "c"], label="d3") #gives options to choose from
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            text1 = gr.Textbox(label="prompt 1")
            text2 = gr.Textbox(label="prompt 2")
            inbtw = gr.Button("Between")
            text4 = gr.Textbox(label="prompt 1")
            text5 = gr.Textbox(label="prompt 2")
        with gr.Column(scale=2, min_width=600):
            img1 = gr.Image("images/cheetah.jpg")
            btn = gr.Button("Go")

demo3.launch()

#more complex layout is possible like css 

with gr.Blocks() as demo4:
    im = gr.ImageEditor(
        width="50vw", #viewport width
    )

demo4.launch()

#actual css units can be used
css = """
.container {
    height: 100vh;
}
"""

with gr.Blocks(css=css) as demo5:
    with gr.Column(elem_classes=["container"]): #elem_classes imports css classes
        name = gr.Chatbot(value=[["1", "2"]], height="70%") #height can be used as percentage

demo5.launch()

#using tabs and accordions
import numpy as np

def flip_text(x):
    return x[::-1]


def flip_image(x):
    return np.fliplr(x)


with gr.Blocks() as demo6:
    gr.Markdown("Flip text or image files using this demo.")
    with gr.Tab("Flip Text"):
        text_input = gr.Textbox()
        text_output = gr.Textbox()
        text_button = gr.Button("Flip")
    with gr.Tab("Flip Image"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

    with gr.Accordion("Open for More!"): #accordion is a collapsible container
        gr.Markdown("Look at me...")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

demo6.launch()

#using sliders to control the number of components
max_textboxes = 10

def variable_outputs(k):
    k = int(k)
    return [gr.Textbox(visible=True)]*k + [gr.Textbox(visible=False)]*(max_textboxes-k)

with gr.Blocks() as demo7:
    s = gr.Slider(1, max_textboxes, value=max_textboxes, step=1, label="How many textboxes to show:")
    textboxes = []
    for i in range(max_textboxes):
        t = gr.Textbox(f"Textbox {i}")
        textboxes.append(t)

    s.change(variable_outputs, s, textboxes)

#defining the component but rendering it later 
    
input_textbox = gr.Textbox()

with gr.Blocks() as demo8:
    gr.Examples(["hello", "bonjour", "merhaba"], input_textbox)
    input_textbox.render() #use render to render the component