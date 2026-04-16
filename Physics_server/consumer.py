from kafka import KafkaConsumer
import json
import requests

KAFKA_SERVER = "localhost:9092"
TOPIC = "query_topic"

# ---------------- OLLAMA CALL ----------------
def call_mistral(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    return response.json()["response"]


# ---------------- CONSUMER ----------------
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Physics consumer started...")

for msg in consumer:

    data = msg.value

    if data["domain"] == "physics":

        query = data["query"]

        print("Received:", query)

        prompt = f"""
        You are a physics expert.
        Explain clearly:

        {query}
        """

        answer = call_mistral(prompt)

        print("Answer:", answer)