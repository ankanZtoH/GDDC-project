# client.py

import requests

SERVER_URL = "http://10.65.22.42:8000/query"

while True:
    query = input("\nEnter your question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    try:
        response = requests.get(SERVER_URL, params={"q": query})
        data = response.json()

        print("\n--- RESPONSE ---")
        print("Answer:", data)

    except Exception as e:
        print("Error:", e)