import json
import requests
from groq import Groq

client = Groq()

# Replace with your actual HF Space URL
HF_SPACE_URL = "https://YOUR-USERNAME-YOUR-SPACE.hf.space/api/predict"

tools = [
    {
        "type": "function",
        "function": {
            "name": "celsius_to_fahrenheit",
            "description": "Convert a temperature from Celsius to Fahrenheit using a remote API",
            "parameters": {
                "type": "object",
                "properties": {
                    "celsius": {"type": "number", "description": "Temperature in Celsius"}
                },
                "required": ["celsius"],
            },
        },
    },
]


def celsius_to_fahrenheit(celsius: float) -> dict:
    resp = requests.post(HF_SPACE_URL, json={"data": [celsius]})
    result = resp.json()["data"][0]
    return {"celsius": celsius, "fahrenheit": result}


tool_functions = {
    "celsius_to_fahrenheit": celsius_to_fahrenheit,
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
    run("What is 8.8 degrees Celsius in Fahrenheit?")
