# test_openai.py
from openai import OpenAI

# Create a client (it will read your API key from env OPENAI_API_KEY if set)
client = OpenAI(api_key="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")  # <-- replace with your key, or remove and set env var

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello if you can read this."}
        ],
    )
    print("✅ API call succeeded!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("❌ API call failed!")
    print(e)
