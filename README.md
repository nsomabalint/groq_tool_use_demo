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
