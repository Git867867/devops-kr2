# KR2: Magomerzaev
import os
import socket

import redis
from flask import Flask, request

app = Flask(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD"),
    socket_connect_timeout=2,
    decode_responses=True,
)


@app.route("/health")
def health():
    return "ok\n"


@app.route("/")
def index():
    hits = r.incr("hits")
    student = os.getenv("STUDENT", "unknown")
    return f"KR2 | {student} | container {socket.gethostname()} | hits: {hits}\n"


@app.route("/whoami")
def whoami():
    return (
        f"scheme: {request.headers.get('X-Forwarded-Proto', 'none')}\n"
        f"client: {request.headers.get('X-Real-IP', 'none')}\n"
        f"host: {request.headers.get('Host', 'none')}\n"
    )
