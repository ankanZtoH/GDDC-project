from google import genai
import json
import re

client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group()
    return text

def classify(query):

    prompt = f"""
    You are a strict classifier.

    Classify into:
    math, physics, biology, general

    Return ONLY JSON:
    {{
      "domain": "...",
      "confidence": 0-1
    }}

    Query: {query}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text
    text = extract_json(text)

    try:
        return json.loads(text)
    except:
        return {"domain": "general", "confidence": 0.5}


print(classify("Can you explain the concept of entropy both in thermodynamics and in information theory, and how the meaning differs in these contexts?"))