from flask import Flask, render_template, request, jsonify
from diagram_generator import generate_diagram

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        code = request.json.get("code", "")
        img_base64 = generate_diagram(code)
        if img_base64:
            return jsonify({"success": True, "image": img_base64})
        else:
            return jsonify({"success": False, "error": "Failed to generate diagram"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
