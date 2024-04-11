import json

import requests

url = "http://localhost:8080/stream_jsonl"

print(
    "Not using response streaming. It waits for the entire response to be received before returning (approx 10 seconds). Then I have to split the response by line and parse each line as JSON.")
resp = requests.get(url)
for line in resp.text.split("\n"):
    line=line.strip()
    if line:
        d = json.loads(line)
        print(d, type(d))

print("Using response streaming. It parse every line received as a json object")
resp = requests.get(url, stream=True)
for line in resp.iter_lines():
    # line.decode converts bytes to string
    line = line.decode()
    d = json.loads(line)
    print(d, type(d))
