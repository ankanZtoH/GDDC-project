#=====================================================================================

################ KAFKA #############################

#=======================================================================================================================================================================


from fastapi import FastAPI
import requests
from kafka import KafkaProducer
import json
import re

app = FastAPI()

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
TIMEOUT = 120

# Kafka Config
KAFKA_SERVER = "localhost:9092"
TOPIC = "query_topic"

# ---------------- KAFKA PRODUCER ----------------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# ---------------- OLLAMA CALL ----------------
def call_tinyllama(prompt):

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=TIMEOUT
        )

        return response.json()["response"]

    except Exception as e:
        print("TinyLlama ERROR:", e)
        return ""


# ---------------- CLASSIFIER ----------------
def classify(query):

    q = query.lower()

    # ✅ RULE BASED FIRST
    if any(x in q for x in ["force", "law", "newton", "motion"]):
        return "physics"
    if any(x in q for x in ["derivative", "integral"]):
        return "math"
    if any(x in q for x in ["dna", "cell", "reproduction"]):
        return "biology"

    # fallback to LLM
    prompt = f"""
    Return ONLY ONE WORD:
    math physics biology general

    Query: {query}
    """

    result = call_tinyllama(prompt).lower()

    match = re.search(r"\b(math|physics|biology|general)\b", result)

    if match:
        return match.group(1)

    return "general"


# ---------------- MAIN ROUTER ----------------
def handle_query(query):

    # Step 1: classify
    domain = classify(query)

    # Step 2: send to Kafka
    message = {
        "query": query,
        "domain": domain
    }

    producer.send(TOPIC, message)
    producer.flush()

    # Step 3: return immediately (async system)
    return {
        "query": query,
        "domain": domain,
        "status": "Sent to Kafka (processing...)"
    }


# ---------------- API ----------------
@app.post("/ask")
def ask(data: dict):

    query = data.get("query", "")

    if not query:
        return {"error": "Query is required"}

    return handle_query(query)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# from fastapi import FastAPI
# import requests

# app = FastAPI()

# # ---------------- CONFIG ----------------
# OLLAMA_URL = "http://localhost:11434/api/generate"

# MATH_URL = "http://localhost:8001/solve"
# PHYSICS_URL = "http://localhost:8002/solve"
# BIOLOGY_URL = "http://localhost:8003/solve"

# TIMEOUT = 120


# # ---------------- OLLAMA CALL ----------------
# def call_tinyllama(prompt):

#     try:
#         response = requests.post(
#             OLLAMA_URL,
#             json={
#                 "model": "tinyllama",
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=TIMEOUT
#         )

#         return response.json()["response"]

#     except Exception as e:
#         print("TinyLlama ERROR:", e)
#         return ""


# import re
# def classify(query):

#     q = query.lower()

#     # ✅ RULE BASED FIRST (VERY IMPORTANT)
#     if any(x in q for x in ["force", "law", "newton", "motion"]):
#         return "physics"
#     if any(x in q for x in ["derivative", "integral"]):
#         return "math"
#     if any(x in q for x in ["dna", "cell", "reproduction"]):
#         return "biology"

#     # fallback to LLM
#     prompt = f"""
#     Return ONLY ONE WORD:
#     math physics biology general

#     Query: {query}
#     """

#     result = call_tinyllama(prompt).lower()

#     match = re.search(r"\b(math|physics|biology|general)\b", result)

#     if match:
#         return match.group(1)

#     return "general"

# # ---------------- SERVICE CALL ----------------
# def call_service(url, query):

#     try:
#         res = requests.post(
#             url,
#             json={"query": query},
#             timeout=TIMEOUT
#         )

#         return res.json().get("answer", "No response")

#     except Exception as e:
#         print("Service ERROR:", e)
#         return "Service unavailable"


# # ---------------- MAIN ROUTER ----------------
# def handle_query(query):

#     # Step 1: classify
#     domain = classify(query)

#     # Step 2: route
#     if domain == "math":
#         answer = call_service(MATH_URL, query)

#     elif domain == "physics":
#         answer = call_service(PHYSICS_URL, query)

#     elif domain == "biology":
#         answer = call_service(BIOLOGY_URL, query)

#     else:
#         answer = "Handled by general system"

#     # Step 3: response
#     return {
#         "query": query,
#         "domain": domain,
#         "response": answer
#     }


# # ---------------- API ----------------
# @app.post("/ask")
# def ask(data: dict):

#     query = data.get("query", "")

#     if not query:
#         return {"error": "Query is required"}

#     return handle_query(query)



















































# # from fastapi import FastAPI
# # import requests
# # from google import genai
# # import json
# # # from dotenv import load_dotenv
# # import os
# # import time

# # # ---------------- CONFIG ----------------
# # app = FastAPI()

# # # ✅ Use environment variable (IMPORTANT)
# # # client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# # # import os

# # # load_dotenv(".env.local")   # 👈 load file

# # client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

# # MATH_URL = "http://localhost:8001/solve"
# # PHYSICS_URL = "http://localhost:8002/solve"
# # BIOLOGY_URL = "http://localhost:8003/solve"

# # TIMEOUT = 5


# # # ---------------- HELPER: JSON CLEAN ----------------
# # def extract_json(text: str):
# #     try:
# #         start = text.index("{")
# #         end = text.rindex("}") + 1
# #         return text[start:end]
# #     except:
# #         return "{}"


# # # ---------------- RULE-BASED FALLBACK ----------------
# # def fallback_rule(query):
# #     q = query.lower()

# #     if any(word in q for word in ["force", "law", "motion", "energy"]):
# #         return "physics"
# #     if any(word in q for word in ["derivative", "integral"]):
# #         return "math"
# #     if any(word in q for word in ["dna", "cell", "reproduction"]):
# #         return "biology"

# #     return "general"


# # # ---------------- CLASSIFIER ----------------
# # def classify(query):

# #     prompt = f"""
# #     You are a STRICT domain classifier.

# #     Classify the query into EXACTLY ONE domain:
# #     - math
# #     - physics
# #     - biology
# #     - general

# #     Rules:
# #     - Questions about force, motion, laws, energy → physics
# #     - Questions about derivatives, integrals → math
# #     - Questions about cells, DNA, reproduction → biology
# #     - Only choose "general" if none match

# #     Return ONLY JSON:
# #     {{ "domain": "physics" }}

# #     Query: {query}
# #     """

# #     try:
# #         response = client.models.generate_content(
# #             model="gemini-2.5-flash",
# #             contents=prompt,
# #             config={"temperature": 0}
# #         )

# #         print("\nRAW GEMINI:", response.text)

# #         text = extract_json(response.text)
# #         data = json.loads(text)

# #         domain = data.get("domain", "general").lower()

# #         if domain not in ["math", "physics", "biology", "general"]:
# #             return fallback_rule(query)

# #         return domain

# #     except Exception as e:
# #         print("Classifier ERROR:", e)
# #         return fallback_rule(query)


# # # ---------------- SERVICE CALL ----------------
# # def call_service(url, query):

# #     try:
# #         res = requests.post(
# #             url,
# #             json={"query": query},
# #             timeout=TIMEOUT
# #         )

# #         return res.json().get("answer", "No response")

# #     except Exception as e:
# #         print("Service call failed:", e)
# #         return "Service unavailable"


# # # ---------------- ROUTER ----------------
# # @app.post("/ask")
# # def ask(data: dict):

# #     query = data.get("query", "")

# #     if not query:
# #         return {"error": "Query is required"}

# #     # Step 1: classify
# #     domain = classify(query)

# #     # Step 2: route
# #     if domain == "math":
# #         answer = call_service(MATH_URL, query)

# #     elif domain == "physics":
# #         answer = call_service(PHYSICS_URL, query)

# #     elif domain == "biology":
# #         answer = call_service(BIOLOGY_URL, query)

# #     else:
# #         answer = "Handled by general system"

# #     # Step 3: response
# #     return {
# #         "query": query,
# #         "domain": domain,
# #         "response": answer
# #     }






























# import requests

# def call_tinyllama(prompt):

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "tinyllama",
#             "prompt": prompt,
#             "stream": False
#         },
#         timeout=30
#     )

#     return response.json()["response"]


# def classify(query):

#     prompt = f"""
#     Classify the query into ONE domain:
#     math, physics, biology, general

#     ONLY return ONE word.

#     Query: {query}
#     """

#     result = call_tinyllama(prompt).lower()

#     # robust parsing
#     if "math" in result:
#         return "math"
#     elif "physics" in result:
#         return "physics"
#     elif "biology" in result:
#         return "biology"
#     else:
#         return "general"