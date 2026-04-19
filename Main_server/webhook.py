from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from kafka import KafkaProducer
import requests
import json
import re
import os

app = FastAPI()

# ---------------- UI SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
TIMEOUT = 60

KAFKA_SERVER = "localhost:9092"

# ---------------- KAFKA PRODUCER ----------------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


# ---------------- OLLAMA CALL ----------------
def call_llama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",   # or tinyllama for speed
                "prompt": prompt,
                "stream": False
            },
            timeout=TIMEOUT
        )
        return response.json().get("response", "")
    except Exception as e:
        print("LLM ERROR:", e)
        return ""


# ---------------- CLASSIFIER ----------------
def classify(query):
    q = query.lower()

    # ✅ Rule-based (fast + reliable)
    if any(x in q for x in ["force", "law", "newton", "motion", "gravity"]):
        return "physics"

    if any(x in q for x in ["derivative", "integral", "equation", "solve"]):
        return "math"

    if any(x in q for x in ["dna", "cell", "reproduction"]):
        return "biology"

    # 🤖 fallback LLM
    prompt = f"""
    Classify STRICTLY.

    Return EXACTLY one word:
    math OR physics OR biology OR general

    NO explanation.

    Examples:
    "matrix multiplication" → math
    "newton law" → physics
    "dna replication" → biology


    Query: {query}
    """

    result = call_llama(prompt).lower()

    match = re.search(r"\b(math|physics|biology|general)\b", result)

    if match:
        return match.group(1)

    return "general"


# ---------------- KAFKA ROUTING ----------------
def send_to_kafka(query, domain):
    try:
        if domain == "physics":
            producer.send("physics_topic", {
                "query": query,
                "callback_url": "http://172.20.251.85:8000/receive"

                })

        elif domain == "math":
            producer.send("math_topic", {"query": query})

        elif domain == "biology":
            producer.send("biology_topic", {"query": query})

        else:
            producer.send("general_topic", {"query": query})

        producer.flush()

    except Exception as e:
        print("Kafka ERROR:", e)


# ---------------- MAIN LOGIC ----------------
def handle_query(query):
    domain = classify(query)

    send_to_kafka(query, domain)

    return {
        "query": query,
        "domain": domain,
        "status": "Sent to Kafka (processing...)"
    }


# ---------------- API ----------------
@app.post("/ask")
def ask(data: dict):
    query = data.get("query", "").strip()

    if not query:
        return {"error": "Query is required"}

    return handle_query(query)