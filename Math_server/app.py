from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()
client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

class Query(BaseModel):
    query: str
import time

def call_gemini(prompt):

    for i in range(3):  # retry 3 times
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Retry {i+1}: {e}")
            time.sleep(2)

    return "Math service temporarily unavailable (Gemini busy)"


@app.post("/solve")
def solve(data: Query):

    prompt = f"""
    You are a mathematics expert.

    Solve only the math part of this query:
    {data.query}
    """

    answer = call_gemini(prompt)

    return {"domain": "math", "answer": answer}