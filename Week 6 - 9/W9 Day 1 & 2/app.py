import json
import time


def greet(name: str) -> str:
    return f"Hello, {name}"


def lambda_handler(event, context):
    name = event.get("name", "Stranger")
    message = greet(name=name)
    print(message)
    return {"statusCode": 200, "body": json.dumps({"message": message})}


if __name__ == "__main__":
    while True:
        time.sleep(5)
        print("WAITING")
        break
    print(greet(name="Carlos"))
