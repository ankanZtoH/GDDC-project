from kafka import KafkaConsumer
import json
import requests

# ---------------- CONFIG ----------------
KAFKA_SERVER = "192.168.1.10:9092"   # 🔥 Kafka machine IP
TOPIC = "query_topic"


# ---------------- MODEL CALL ----------------
def call_model(prompt):

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",   # 🔥 faster than mistral
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        return response.json()["response"]

    except Exception as e:
        return f"Error: {str(e)}"


# ---------------- KAFKA CONSUMER ----------------
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Math consumer started...")


# ---------------- MAIN LOOP ----------------
for msg in consumer:

    data = msg.value

    # 👉 Only handle math queries
    if data.get("domain") == "math":

        query = data.get("query")

        print("\nReceived:", query)

        prompt = f"""
        You are a mathematics expert.

        Solve step by step:

        {query}
        """

        answer = call_model(prompt)

        print("Answer:", answer)