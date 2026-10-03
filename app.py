import os

from flask import Flask, Response, jsonify
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    generate_latest,
)

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "sit223_http_requests_total",
    "Total number of HTTP requests received",
    ["endpoint", "status"],
)


@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/", status="200").inc()

    return jsonify({
        "message": "SIT223 DevOps Project is running",
        "status": "success",
    })


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health", status="200").inc()

    return jsonify({
        "status": "healthy",
    }), 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
    )
