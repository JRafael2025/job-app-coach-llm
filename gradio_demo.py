import gradio as gr

def combine(a, b):
    return a + " " + b

demo = gr.Interface(
    fn=combine,
    inputs = [
        gr.Textbox(label="Input 1"),
        gr.Textbox(label="Input 2")
    ],
    outputs = gr.Textbox(value="", label="Output")
)
demo.launch(server_name="0.0.0.0", server_port= 7860)