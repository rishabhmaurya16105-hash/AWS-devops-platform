from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

APP_NAME = "aws-devops-platform"
APP_VERSION = "1.0.0"


@app.route("/")
def home():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "message": "AWS DevOps Platform is running",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/info")
def info():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": "development",
        }
    )

@app.route("/error")
def error():
    return jsonify({"status": "internal server error"}), 500

@app.after_request
def record_request(response):
    if request.path != "/metrics":
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code,
        ).inc()
    return response


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
