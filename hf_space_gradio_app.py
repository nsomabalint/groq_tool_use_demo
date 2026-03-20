import gradio as gr


def celsius_to_fahrenheit(celsius):
    return round(celsius * 9 / 5 + 32, 1)


gr.Interface(fn=celsius_to_fahrenheit, inputs="number", outputs="number").launch()
