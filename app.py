"""
app.py — Recster Flask API
==========================

Single POST /recommend endpoint that runs the LangGraph agent and returns
music recommendations plus the intermediate tool steps.

Usage:
    python app.py          # starts on http://localhost:5000
"""

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage

from src.agent import executor, reset_agent_state

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)
    if not data or "description" not in data:
        return jsonify({"error": "Request body must include a 'description' field."}), 400

    description = data["description"].strip()
    if not description:
        return jsonify({"error": "'description' cannot be empty."}), 400

    reset_agent_state()

    try:
        result = executor.invoke({"messages": [("user", description)]})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Agent failed.", "detail": str(e)}), 500

    tool_messages = [m for m in result["messages"] if isinstance(m, ToolMessage)]

    recommendations = []
    for msg in reversed(tool_messages):
        if msg.name == "get_recommendations":
            try:
                recs = json.loads(msg.content)
                if isinstance(recs, list) and recs and "error" not in recs[0]:
                    recommendations = recs
            except (json.JSONDecodeError, IndexError):
                pass
            break

    steps = [{"step": msg.name, "output": msg.content} for msg in tool_messages]

    return jsonify({"recommendations": recommendations, "steps": steps})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
