from flask import Blueprint, request, jsonify, session
import json
import os

limits_api = Blueprint("limits_api", __name__)

LIMITS_FILE = "daily_limits.json"

def load_limits():
    if os.path.exists(LIMITS_FILE):
        with open(LIMITS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_limits(data):
    with open(LIMITS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@limits_api.route("/api/save-limits", methods=["POST"])
def save_daily_limits():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    content = request.get_json()
    user = session["user"]
    date = content.get("date")

    if not date:
        return jsonify({"error": "Date is required"}), 400

    data = load_limits()
    data.setdefault(user, {})
    data[user][date] = {
        "calories": content.get("calories", 0),
        "protein": content.get("protein", 0),
        "fat": content.get("fat", 0),
    }
    save_limits(data)
    return jsonify({"message": "Limits saved successfully!"})


@limits_api.route("/api/get-limits")
def get_daily_limits():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user = session["user"]
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Date is required"}), 400

    data = load_limits()
    user_data = data.get(user, {})
    return jsonify(user_data.get(date, {}))
