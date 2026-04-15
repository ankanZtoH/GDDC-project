from google import genai

client = genai.Client(api_key="AIzaSyCjPKpPbdZWBXLu6taF8vJNkKTMK7Vw7tM")

for m in client.models.list():
    print(m.name)