from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import requests
import tempfile
from PIL import Image
import uuid
from flask_session import Session

# Load environment variables
load_dotenv()

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_users(users_dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users_dict, f)

DAILY_LIMITS_FILE = "daily_limits.json"

def load_daily_limits():
    if not os.path.exists(DAILY_LIMITS_FILE):
        return {}
    with open(DAILY_LIMITS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_daily_limits(data):
    with open(DAILY_LIMITS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "devkey")  # Change to strong key in prod
app.config['UPLOAD_FOLDER'] = os.path.join("static", "uploads")

# ✅ Configure Flask-Session (server-side sessions, not in cookies)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session"  # optional: store in folder
Session(app)

# Load Gemini API key from .env
GEMINI_API_KEY = os.getenv("MY_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found in .env!")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  

def get_calories_from_image(image_path):
    """
    Use Gemini API to recognize food and estimate calories.
    Returns structured JSON, with a fallback if no food is detected.
    """
    img = Image.open(image_path)

    prompt = (
        "Identify all food items in this image and estimate calories, protein, and fat for each. "
        "Respond ONLY in JSON with the following structure:\n"
        "{\n"
        '  "food_items": [\n'
        "    {\"name\": \"food name\", \"calories\": 0, \"protein\": 0, \"fat\": 0}\n"
        "  ],\n"
        '  "total": 0,\n'
        '  "reasoning": "Explain briefly how you estimated calories"\n'
        "}"
    )

    response = model.generate_content([img, prompt])
    text = response.text

    # --- Try to extract JSON from response ---
    try:
        # Sometimes Gemini adds extra text; extract JSON block
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        result_data = json.loads(json_text)
    except Exception as e:
        print("⚠️ JSON parse error:", e)
        result_data = {"food_items": [], "total": 0, "reasoning": text}

    # --- Fallback if no food items detected ---
    if not result_data.get("food_items"):
        result_data["food_items"] = [
            {"name": "Unknown food", "calories": 0, "protein": 0, "fat": 0}
        ]
        result_data["reasoning"] = (
            "Gemini could not recognize any food in the image. "
            "Try using a simpler image or clearer food items."
        )
        result_data["total"] = 0

    # --- Calculate total if items exist ---
    else:
        total_calories = sum(item.get("calories", 0) for item in result_data["food_items"])
        result_data["total"] = total_calories

    return result_data

def get_calories_from_url(image_url):
    """Download image from URL and process with Gemini."""
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(r.content)
            tmp_path = tmp.name

        img = Image.open(tmp_path)  # ✅ Open as PIL.Image
        return get_calories_from_image(tmp_path)  # Reuse same function
    else:
        raise Exception("Failed to download image")

# ---------- Flask Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clear_session")
def clear_session():
    session.clear()
    flash("Session cleared!", "info")
    return redirect(url_for("index"))

@app.before_request
def check_session_size():
    size = len(str(session))
    if size > 1000:
        print("⚠️ SESSION SIZE:", size, "bytes")

@app.route("/scan", methods=["POST"])
def scan():
    if "file" not in request.files and not request.form.get("image_url"):
        flash("No file or image URL provided", "error")
        return redirect(url_for("index"))

    image_path = None
    image_url = None

    # --- Handle file upload ---
    if "file" in request.files and request.files["file"].filename != "":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image_path = filepath

    # --- Handle image URL ---
    elif request.form.get("image_url"):
        image_url = request.form.get("image_url")
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            # ✅ Save URL image into static/uploads
            filename = str(uuid.uuid4()) + ".jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "wb") as f:
                f.write(r.content)
            image_path = filepath
        else:
            flash("Failed to download image.", "error")
            return redirect(url_for("index"))

    else:
        flash("No file or image URL provided", "error")
        return redirect(url_for("index"))

    # --- Process image ---
    result_data = get_calories_from_image(image_path)

    # --- Save result to file with UUID ---
    scan_id = str(uuid.uuid4())
    tmp_dir = "temp_results"
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_file_path = os.path.join(tmp_dir, f"{scan_id}.json")

    with open(tmp_file_path, "w") as f:
        json.dump(result_data, f)

    # ✅ Redirect with scan_id and uploaded filename
    return redirect(url_for(
        "scan_result_page",
        scan_id=scan_id,
        image_url=image_url or "",
        uploaded_filename=os.path.basename(image_path) if image_path else ""
    ))

@app.route("/scan_result")
def scan_result_page():
    scan_id = request.args.get("scan_id")
    image_url = request.args.get("image_url")
    uploaded_filename = request.args.get("uploaded_filename")

    if uploaded_filename == "":
        uploaded_filename = None  # avoid broken link

    # load result
    tmp_file_path = os.path.join("temp_results", f"{scan_id}.json")
    if not os.path.exists(tmp_file_path):
        flash("Scan result missing!", "error")
        return redirect(url_for("index"))

    with open(tmp_file_path, "r") as f:
        result = json.load(f)

    os.remove(tmp_file_path)

    return render_template(
        "scan_result.html",
        result=result,
        image_url=image_url,
        uploaded_filename=uploaded_filename
    )

@app.route("/calorie-counter")
def calorie_counter():
    if "user" not in session:
        flash("You must be logged in to access the calorie counter.", "error")
        return redirect(url_for("login"))
    return render_template("calorie-counter.html", logged_in=True, user=session["user"])

# Dummy "user database"
users = load_users()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email not in users:
            flash("Email does not exist. Please Sign Up!", "error")
            return redirect(url_for("signup"))

        if check_password_hash(users[email], password):
            session["user"] = email
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Wrong password. Try again.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirmPassword"]

        if email in users:
            flash("Email already registered. Please Login!", "error")
            return redirect(url_for("login"))

        if password != confirm:
            flash("Passwords do not match", "error")
            return redirect(url_for("signup"))

        users[email] = generate_password_hash(password)
        save_users(users)
        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("index"))

@app.route("/api/save-limits", methods=["POST"])
def api_save_limits():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    date = data.get("date")
    calories = data.get("calories")
    protein = data.get("protein")
    fat = data.get("fat")

    if not date:
        return jsonify({"error": "Missing date"}), 400

    all_limits = load_daily_limits()
    user_email = session["user"]

    if user_email not in all_limits:
        all_limits[user_email] = {}

    all_limits[user_email][date] = {
        "calories": calories,
        "protein": protein,
        "fat": fat
    }

    save_daily_limits(all_limits)
    return jsonify({"message": "Saved successfully"})

@app.route("/api/get-limits")
def api_get_limits():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Missing date"}), 400

    all_limits = load_daily_limits()
    user_email = session["user"]

    user_limits = all_limits.get(user_email, {}).get(date)
    if user_limits:
        return jsonify(user_limits)
    else:
        return jsonify({})

# ---------- Run Server ----------
if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists("temp_results"):
        os.makedirs("temp_results")
    app.run(debug=True)

