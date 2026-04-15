# main_server.py

from fastapi import FastAPI
import requests

app = FastAPI()

def classify(query):
    if "integral" in query:
        return "math"
    return "general"

@app.get("/query")
def handle_query(q: str):
    domain = classify(q)

    if domain == "math":
        url = "http://192.168.1.10:8001/solve"  # Math machine IP
        response = requests.get(url, params={"query": q})
        return response.json()

    return {"answer": "General response"}