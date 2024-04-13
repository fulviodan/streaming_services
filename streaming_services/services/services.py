# A flask app that streams data from a generator
import random
import time

from flask import Flask, Response, request, json, stream_with_context, jsonify

app = Flask("streaming")


@app.get("/stream")
def stream():
    """Stream data from a generator. Shows how to stream a response"""

    def generate():
        for i in range(100):
            time.sleep(0.1)
            yield f"Data point {i}\n"

    return Response(generate(), mimetype="text/plain")


@app.get("/stream_jsonl")
def stream_jsonl():
    """Stream data from a generator. Shows how to stream a response"""

    def generate():
        for i in range(100):
            time.sleep(0.1)
            yield f'{{"data": {i}}}\n'

    return Response(generate(), mimetype="application/jsonlines")


@app.post('/predict')
def predict():
    print("Predictttt")

    def generate_predictions():
        print(request.stream)
        for line in request.stream:
            line = line.decode().strip()
            if line:
                print(line)
                d = json.loads(line)
                time.sleep(0.1)
                d['prediction'] = random.choice([0, 1])
                yield json.dumps(d) + "\n"

    return stream_with_context(generate_predictions(), mimetype="application/jsonl")


@app.get("/negotiate")
def negotiate():
    # Negotiate the content type
    if "text/plain" in request.accept_mimetypes:
        def stream():
            for i in range(100):
                yield f"Data point {i}\n"

        return Response(stream(), mimetype="text/plain")
    # Can be called with curl -H "Accept: application/jsonl" http://localhost:8080/negotiate
    if "application/jsonl" in request.accept_mimetypes:
        def stream_jsonl():
            for i in range(100):
                yield f'{{"data": {i}}}\n'

        return Response(stream_jsonl(), mimetype="application/jsonl")

    if "application/json" in request.accept_mimetypes:
        return jsonify([{"data": i} for i in range(100)])

    raise Exception("No supported content type")


if __name__ == '__main__':
    app.run(port=8080, debug=True)
