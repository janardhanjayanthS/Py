from transformers import pipeline

chat = [
    {"role": "system", "content": "You are a helpful science assistant."},
    {"role": "user", "content": "Hey, can you explain gravity to me?"},
]

pipeline = pipeline(
    task="text-generation",
    model="HuggingFaceH4/zephyr-7b-beta",
    dtype="auto",
    device_map="auto",
)
response = pipeline(chat, max_new_tokens=512)
print("RESPONSE: ", response[0]["generated_text"][-1]["content"])
