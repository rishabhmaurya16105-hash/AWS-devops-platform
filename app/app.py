from flask import Flask, jsonify

app = Flask(__name__)

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
    return jsonify(
        {
            "status": "healthy"
        }
    )


@app.route("/info")
def info():
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": "development",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
