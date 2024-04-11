import requests

url = "http://localhost:8080/stream"

print(
    "Not using response streaming. It waits for the entire response to be received before returning (approx 10 seconds)")
resp = requests.get(url)
print(resp.text)

print("Using response streaming. It returns the response as it is received (approx 1 second)")
resp = requests.get(url, stream=True)
for line in resp.iter_lines():
    # line.decode converts bytes to string
    print(line, line.decode())
