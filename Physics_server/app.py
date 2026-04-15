from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
import time

app = FastAPI()

client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

class Query(BaseModel):
    query: str


# ---------- GEMINI CALL (RETRY + FALLBACK) ----------
def call_gemini(prompt):

    # Retry logic
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"[Retry {i+1}] Gemini error:", e)
            time.sleep(2)

    # Fallback model
    try:
        print("Switching to fallback model...")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Fallback failed:", e)
        return "Physics service temporarily unavailable"


# ---------- API ----------
@app.post("/solve")
def solve(data: Query):

    prompt = f"""
    You are a physics expert.

    ONLY answer physics-related parts of the query.
    Ignore math, biology, or unrelated content.

    Explain clearly and simply.

    Query: {data.query}
    """

    answer = call_gemini(prompt)

    return {
        "domain": "physics",
        "answer": answer
    }