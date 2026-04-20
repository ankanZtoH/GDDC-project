from kafka import KafkaConsumer
import json
import requests

# ---------------- CONFIG ----------------
KAFKA_SERVER = "172.20.251.85:9092"   # 🔥 Kafka machine IP
TOPIC = "math_topic"



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
            timeout=120
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
    callback_url = data.get("callback_url")

    # 👉 Only handle math queries
   
    query = data.get("query")

    print("\nReceived:", query)

    prompt = f"""
        You are a mathematics expert.
        whatever step needed give it in brief

    {query}
        """

    answer = call_model(prompt)

    print("Answer:", answer)

    try:
        if callback_url:
            requests.post(callback_url,json={
                "query": query,
                "answer": answer
            })
    except Exception as e:
        print("Not found")
