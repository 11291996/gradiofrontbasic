import gradio as gr

#live interface
def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2

demo1 = gr.Interface(
    calculator,
    [
        "number",
        gr.Radio(["add", "subtract", "multiply", "divide"]),
        "number"
    ],
    "number",
    live=True, #update live as input changes
)

demo1.launch()

#video streaming
import numpy as np

def flip(im):
    return np.flipud(im)

demo2 = gr.Interface(
    flip, 
    gr.Image(sources=["webcam"], streaming=True), #gradio detects the stream webcam with its streaming image and applies streaming programming 
    "image",
    live=True #live should be also true
)

demo2.launch()

#
from pydub import AudioSegment
from time import sleep

with gr.Blocks() as demo:
    input_audio = gr.Audio(label="Input Audio", type="filepath", format="mp3") 
    with gr.Row():
        with gr.Column():
            stream_as_file_btn = gr.Button("Stream as File")
            format = gr.Radio(["wav", "mp3"], value="wav", label="Format")
            stream_as_file_output = gr.Audio(streaming=True) #this component streams out audio streaming data

            def stream_file(audio_file, format):
                audio = AudioSegment.from_file(audio_file)
                i = 0
                chunk_size = 1000
                while chunk_size * i < len(audio):
                    chunk = audio[chunk_size * i : chunk_size * (i + 1)]
                    i += 1
                    if chunk:
                        file = f"/tmp/{i}.{format}"
                        chunk.export(file, format=format)
                        yield file
                        sleep(0.5)

            stream_as_file_btn.click(
                stream_file, [input_audio, format], stream_as_file_output
            )

            gr.Examples(
                [["audio/cantina.wav", "wav"], ["audio/cantina.wav", "mp3"]],
                [input_audio, format],
                fn=stream_file,
                outputs=stream_as_file_output,
                cache_examples=True,
            )

        with gr.Column():
            stream_as_bytes_btn = gr.Button("Stream as Bytes")
            stream_as_bytes_output = gr.Audio(format="bytes", streaming=True)

            def stream_bytes(audio_file):
                chunk_size = 20_000
                with open(audio_file, "rb") as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if chunk:
                            yield chunk
                            sleep(1)
                        else:
                            break
            stream_as_bytes_btn.click(stream_bytes, input_audio, stream_as_bytes_output)

demo3.queue().launch()