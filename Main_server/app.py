from fastapi import FastAPI
import requests
from google import genai
import json
import re
import os
import time

# ---------------- CONFIG ----------------
app = FastAPI()

# client = genai.Client(api_key=os.getenv("AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM"))
client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

MATH_URL = "http://localhost:8001/solve"
PHYSICS_URL = "http://localhost:8002/solve"
BIOLOGY_URL = "http://localhost:8003/solve"

TIMEOUT = 5


# ---------------- HELPER: JSON CLEAN ----------------
def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group() if match else text


# ---------------- CLASSIFIER ----------------
def classify(query: str) -> str:

    prompt = f"""
    You are a strict classifier.

    Classify the query into EXACTLY ONE domain:
    - math
    - physics
    - biology
    - general

    Rules:
    - Choose ONLY ONE most relevant domain
    - No explanation
    - Return ONLY JSON

    Format:
    {{
      "domain": "math | physics | biology | general"
    }}

    Query: {query}
    """

    for _ in range(3):  # retry logic
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = extract_json(response.text)
            data = json.loads(text)

            return data.get("domain", "general")

        except Exception as e:
            print("Classifier error, retrying:", e)
            time.sleep(2)

    return "general"


# ---------------- SERVICE CALL ----------------
def call_service(url, query):

    try:
        res = requests.post(
            url,
            json={"query": query},
            timeout=TIMEOUT
        )
        return res.json().get("answer", "No response")

    except Exception as e:
        print("Service call failed:", e)
        return "Service unavailable"


# ---------------- ROUTER ----------------
@app.post("/ask")
def ask(data: dict):

    query = data.get("query", "")

    if not query:
        return {"error": "Query is required"}

    # Step 1: classify
    domain = classify(query)

    # Step 2: route
    if domain == "math":
        answer = call_service(MATH_URL, query)

    elif domain == "physics":
        answer = call_service(PHYSICS_URL, query)

    elif domain == "biology":
        answer = call_service(BIOLOGY_URL, query)

    else:
        answer = "Handled by general system"

    # Step 3: return response
    return {
        "query": query,
        "domain": domain,
        "response": answer
    }