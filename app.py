from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "letmein", "monkey", "111111", "iloveyou", "admin"
}

def analyze_password(password):
    """Analyze a password's strength and return a score, feedback, and estimated crack time."""
    score = 0
    feedback = []

    length = len(password)
    if length >= 12:
        score += 25
    elif length >= 8:
        score += 15
        feedback.append("Consider using 12+ characters for better security.")
    else:
        feedback.append("Password is too short. Use at least 8 characters.")

    if re.search(r"[a-z]", password):
        score += 10
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 15
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 15
    else:
        feedback.append("Add numbers.")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 20
    else:
        feedback.append("Add special characters (!, @, #, etc.).")

    if password.lower() in COMMON_PASSWORDS:
        score = max(0, score - 50)
        feedback.append("This is a commonly used password and is very easy to guess.")

    if re.search(r"(.)\1{2,}", password):
        score = max(0, score - 10)
        feedback.append("Avoid repeating the same character multiple times.")

    score = min(100, max(0, score))

    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Moderate"
    elif score >= 20:
        strength = "Weak"
    else:
        strength = "Very Weak"

    crack_time = estimate_crack_time(password)

    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
        "crack_time": crack_time
    }

def estimate_crack_time(password):
    """Rough estimate of time to brute-force crack a password."""
    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset_size += 32

    if charset_size == 0:
        return "Instantly"

    combinations = charset_size ** len(password)
    guesses_per_second = 1_000_000_000  # 1 billion guesses/sec (modern GPU estimate)
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    else:
        years = seconds / 31536000
        if years > 1_000_000:
            return "Millions of years"
        return f"{years:,.0f} years"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")
    result = analyze_password(password)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)