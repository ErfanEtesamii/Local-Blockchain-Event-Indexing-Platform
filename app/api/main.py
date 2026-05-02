from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return {"status": "API is running", "message": "Blockchain data is accessible"}

if __name__ == "__main__":
    # روی همه آی‌پی‌ها و پورت 8080 اجرا می‌شود
    app.run(host="0.0.0.0", port=8080)