import json
import requests
from groq import Groq

client = Groq()

tools = [
    {
        "type": "function",
        "function": {
            "name": "geocode_city",
            "description": "Get latitude and longitude for a city name",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. Budapest"}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location using latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
]


def geocode_city(city: str) -> dict:
    resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
    )
    data = resp.json()
    result = data["results"][0]
    return {"name": result["name"], "latitude": result["latitude"], "longitude": result["longitude"]}


def get_weather(latitude: float, longitude: float) -> dict:
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": latitude, "longitude": longitude, "current_weather": True},
    )
    return resp.json()["current_weather"]


tool_functions = {
    "geocode_city": geocode_city,
    "get_weather": get_weather,
}


def run(user_message: str):
    print(f"\nUser: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            print(f"Assistant: {msg.content}")
            return

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  -> Calling {name}({args})")
            result = tool_functions[name](**args)
            print(f"  <- {json.dumps(result)}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })


if __name__ == "__main__":
    run("What's the weather like in Budapest?")
