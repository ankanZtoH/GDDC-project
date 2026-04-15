# from fastapi import FastAPI
# from pydantic import BaseModel
# from google import genai
# import os
# import time

# app = FastAPI()

# client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

# class Query(BaseModel):
#     query: str


# # ---------- GEMINI CALL (RETRY + FALLBACK) ----------
# # def call_gemini(prompt):

# #     # Retry logic
# #     for i in range(3):
# #         try:
# #             response = client.models.generate_content(
# #                 model="gemini-2.5-flash",
# #                 contents=prompt
# #             )
# #             return response.text

# #         except Exception as e:
# #             print(f"[Retry {i+1}] Gemini error:", e)
# #             time.sleep(2)

# #     # Fallback model
# #     try:
# #         print("Switching to fallback model...")
# #         response = client.models.generate_content(
# #             model="gemini-2.0-flash",
# #             contents=prompt
# #         )
# #         return response.text

# #     except Exception as e:
# #         print("Fallback failed:", e)
# #         return "Physics service temporarily unavailable"



# # import time

# def call_gemini(prompt):

#     # 1️⃣ Try main model
#     for i in range(2):
#         try:
#             response = client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=prompt
#             )
#             return response.text
#         except Exception as e:
#             print("Flash failed:", e)
#             time.sleep(1)

#     # 2️⃣ Try fallback model
#     try:
#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=prompt
#         )
#         return response.text
#     except Exception as e:
#         print("Fallback failed:", e)

#     # 3️⃣ FINAL fallback (IMPORTANT)
#     return "⚠️ Physics service is busy right now. Please try again in a moment."

# # ---------- API ----------
# @app.post("/solve")
# def solve(data: Query):

#     prompt = f"""
#     You are a physics expert.

#     ONLY answer physics-related parts of the query.
#     Ignore math, biology, or unrelated content.

#     Explain clearly and simply.

#     Query: {data.query}
#     """

#     answer = call_gemini(prompt)

#     return {
#         "domain": "physics",
#         "answer": answer
#     }





from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Query(BaseModel):
    query: str



# def call_mistral(prompt):

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "mistral",
#             "prompt": prompt,
#             "stream": False
#         },
#         timeout=60
#     )

#     return response.json()["response"]

import requests

def call_mistral(prompt):

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=120   # 🔥 increase timeout
        )

        return response.json()["response"]

    except requests.exceptions.ReadTimeout:
        return "⚠️ Response taking too long (model slow). Try again."

    except Exception as e:
        return f"Error: {str(e)}"

# @app.post("/solve")
# def solve(data: Query):

#     prompt = f"""
#     You are a physics expert.
#     Explain clearly:

#     {data.query}
#     """

#     answer = call_mistral(prompt)

#     return {"domain": "physics", "answer": answer}

@app.post("/solve")
def solve(data: Query):

    prompt = f"""
    You are a physics expert.
    Explain clearly:

    {data.query}
    """

    answer = call_mistral(prompt)

    return {
        "domain": "physics",
        "answer": answer
    }