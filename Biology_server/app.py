import time
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()
client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

class Query(BaseModel):
    query: str


def call_gemini(prompt):

    for i in range(3):  # retry
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Retry {i+1}:", e)
            time.sleep(2)

    # fallback
    try:
        return client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        ).text
    except:
        return "Biology service temporarily unavailable"


@app.post("/solve")
def solve(data: Query):

    prompt = f"""
    You are a biology expert.

    ONLY answer biology-related parts.

    Query: {data.query}
    """

    answer = call_gemini(prompt)

    return {"domain": "biology", "answer": answer}