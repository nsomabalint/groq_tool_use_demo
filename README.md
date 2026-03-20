# Groq Tool Use Demo

A simple demo of LLM tool calling with Groq. The model chains two API calls — first geocoding a city name, then fetching the weather — using [Open-Meteo](https://open-meteo.com/) (no API key needed).

## Setup

```bash
pip install groq requests
export GROQ_API_KEY="your-key-here"
```

## Usage

```bash
python groq_tool_demo.py
```

## Example output

```
User: What's the weather like in Budapest?
  -> Calling geocode_city({'city': 'Budapest'})
  <- {"name": "Budapest", "latitude": 47.49835, "longitude": 19.04045}
  -> Calling get_weather({'latitude': 47.49835, 'longitude': 19.04045})
  <- {"time": "2026-03-20T06:30", "interval": 900, "temperature": 8.8, "windspeed": 6.5, "winddirection": 16, "is_day": 1, "weathercode": 1}
Assistant: The current weather in Budapest is partly cloudy with a temperature of 8.8 degrees Celsius and a wind speed of 6.5 meters per second.
```

The model first resolves the city to coordinates, then uses those coordinates to get the weather — two chained tool calls in a single conversation turn.

## Using a Hugging Face Space as a tool

Gradio apps automatically expose a REST API at `/api/predict` — you don't need to write any API code yourself. This means any Gradio app deployed on [Hugging Face Spaces](https://huggingface.co/spaces) is already a working API endpoint that an LLM can call as a tool.

### Deploying the Space

`hf_space_gradio_app.py` is a minimal Gradio app that converts Celsius to Fahrenheit. To deploy it:

1. Create a new Space on Hugging Face (select Gradio as the SDK)
2. Upload `hf_space_gradio_app.py` as `app.py`
3. The Space will give you a URL like `https://your-username-your-space.hf.space`

### Calling it as a tool

`hf_space_tool_demo.py` uses that Space as a remote tool. Update `HF_SPACE_URL` with your Space's URL and run:

```bash
python hf_space_tool_demo.py
```

The script sends a POST request to the Space's `/api/predict` endpoint, same as any other tool call — the LLM doesn't know or care that it's hitting a Gradio app behind the scenes.
