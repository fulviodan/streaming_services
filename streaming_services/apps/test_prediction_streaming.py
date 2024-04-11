import json

import requests


def gen(n):
    for i in range(n):
        d = dict(text=f"Example number {i}")
        # returns the string representation of the dictionary and newline character
        temp = json.dumps(d) + "\n"
        yield temp


print("Without streaming")
resp = requests.post("http://localhost:8080/predict", data=gen(100))
print(resp.text)

print("With streaming")
resp = requests.post("http://localhost:8080/predict", data=gen(100), stream=True)
for line in resp.iter_lines():
    d = json.loads(line.decode())
    print(d)
