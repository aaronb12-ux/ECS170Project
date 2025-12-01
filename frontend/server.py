from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    resume = data.get("resume")
    job = data.get("job")

    if resume is None:
        return jsonify({"error": "resume missing"}), 400
    if job is None:
        return jsonify({"error": "job missing"}), 400

    response = {
        "match_score": 0.78,
        "summary": "Hard-coded analysis result. Replace with real logic.",
        "highlights": [
            {"type": "skill_match", "text": "Python", "weight": 0.9},
            {"type": "experience_match", "text": "Web development", "weight": 0.75}
        ],
        "resume_length": len(resume),
        "job_length": len(job)
    }
    return jsonify(response), 200

@app.route("/", methods=["GET"])
def index():
    return "Resume Analyzer API (local). POST /api/analyze with JSON {resume, job}", 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

