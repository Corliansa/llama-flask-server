from flask import Flask, request
from llama_cpp import Llama
import os

app = Flask(__name__)
app.logger.setLevel("INFO")


@app.route("/")
def home():
    return {"message": "Hello, World!"}


@app.route("/llama", methods=["POST"])
def generate_cta():
    try:
        # Check if request method is POST
        if request.method != "POST":
            return "Method Not Allowed", 405

        # Parse incoming data as binary
        data = request.get_data()
        text = data.decode("utf-8")
        llm = Llama(model_path=os.environ.get("LLAMA_MODEL_PATH"))
        response = llm(text)
        result = {
            "text": response,
        }

        # Respond with success message
        return {"result": result}, 200
    except Exception as e:
        app.logger.error(f"Command to action error: {e}")
        return {"error": "Internal Server Error"}, 500


if __name__ == "__main__":
    app.run(host="::", port=3003, debug=True)
