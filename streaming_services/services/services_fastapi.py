import io

from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, JSONResponse
import random
import time
import json

app = FastAPI()


async def read_lines(stream):
    buffer = ""
    async for chunk in stream:
        buffer += chunk.decode()
        lines = buffer.split("\n")
        for line in lines[:-1]:
            yield line + "\n"
        buffer = lines[-1]


def generate_plain():
    for i in range(100):
        yield f"Data point {i}\n"


def generate_jsonl():
    for i in range(100):
        yield json.dumps({"data": i}) + "\n"


@app.get("/stream")
def stream():
    return StreamingResponse(generate_plain(), media_type="text/plain")


@app.get("/stream_jsonl")
def stream_jsonl():
    return StreamingResponse(generate_jsonl(), media_type="application/jsonlines")


@app.post("/predict")
async def predict(request: Request):
    async def generate_predictions():
        async for line in read_lines(request.stream()):
            line = line.strip()
            if line:
                d = json.loads(line)
                time.sleep(0.1)
                d['prediction'] = random.choice([0, 1])
                yield json.dumps(d) + "\n"

    return StreamingResponse(generate_predictions(), media_type="application/jsonl")


@app.get("/negotiate")
def negotiate(request: Request):
    accept = request.headers.get("accept", "")
    if "text/plain" in accept or "*/*" in accept:
        return StreamingResponse(generate_plain(), media_type="text/plain")
    elif "application/jsonl" in accept:
        return StreamingResponse(generate_jsonl(), media_type="application/jsonl")
    elif "application/json" in accept:
        return JSONResponse([{"data": i} for i in range(100)])
    else:
        return Response(content="No supported content type", status_code=406)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
