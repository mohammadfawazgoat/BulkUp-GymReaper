import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = "gym.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

current_date = datetime.now().strftime("%y-%m-%d")

@app.route("/")
def index():
    return render_template("index.html")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    db = get_db()
    name = request.form.get("Name")
    password = request.form.get("Password")
    number = request.form.get("number")
    confirm_password = request.form.get("cPassword")

    if not name or not password or not number:
        flash("Please fill all fields")
        return redirect("/register")
    if password != confirm_password:
        flash("Passwords do not match")
        return redirect("/register")

    hash_password = generate_password_hash(password)
    check_name = db.execute("SELECT name FROM users WHERE name = ?", (name.lower(),)).fetchone()
    if not check_name:
        db.execute("INSERT INTO users(name,password,number,date,oriname) VALUES(?,?,?,?,?)",
                   (name.lower(), hash_password, number, current_date, name))
        db.commit()
    else:
        flash("User already exists")
        return redirect("/register")

    user_id = db.execute("SELECT id FROM users WHERE name = ?", (name.lower(),)).fetchone()["id"]
    session["user_id"] = user_id
    session["user_name"] = name
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    db = get_db()
    name = request.form.get("Name").lower()
    password = request.form.get("Password")

    if not name or not password:
        flash("Please Fill All Fields")
        return redirect("/login")
    user = db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
    if not user or not check_password_hash(user["password"], password):
        flash("Invalid Credentials")
        return redirect("/login")

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["oriname"]
    return redirect("/")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    db = get_db()
    if request.method == "GET":
        return render_template("forgot.html")

    number = request.form.get("number")
    cpassword = request.form.get("cPassword")
    new_password = request.form.get("newPassword")

    if not number or not new_password or not cpassword:
        flash("Please Fill All Fields")
        return redirect("/forgot_password")

    cnumber = db.execute("SELECT number FROM users WHERE number = ?", (number,)).fetchone()
    if not cnumber:
        flash("Number not found")
        return redirect("/forgot_password")
    if new_password != cpassword:
        flash("Passwords Dont Match")
        return redirect("/forgot_password")

    db.execute("UPDATE users SET password = ? WHERE number = ?", (generate_password_hash(new_password), number))
    db.commit()
    return redirect("/login")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    db = get_db()
    track_data = db.execute("SELECT track FROM number WHERE user_id = ?", (session["user_id"],)).fetchone()
    track = track_data["track"] if track_data else 0
    return render_template("dashboard.html", track=track)

@app.route('/progress', methods=['GET'])
def progress():
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calories = [2000, 2150, 2100, 1800, 2200, 2400, 2000]
    workouts = [1, 1, 0, 1, 1, 1, 0]
    return render_template("progress.html", labels=labels, calories=calories, workouts=workouts)

@app.route('/workouts', methods=["GET", "POST"])
def workouts():
    return render_template("workouts.html")

@app.route('/info', methods=["GET", "POST"])
def info():
    db = get_db()
    if request.method == "GET":
        return render_template("info.html")

    name = request.form.get("Name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    height = request.form.get("height")
    weight = request.form.get("weight")
    fitness_goal = request.form.get("fitnessgoal")
    activity_level = request.form.get("activity")

    if not all([name, age, gender, height, weight, fitness_goal, activity_level]):
        flash("Please fill all fields")
        return redirect("/info")

    info_check = db.execute("SELECT id FROM personal_info WHERE id = ?", (session["user_id"],)).fetchone()
    if info_check:
        db.execute("""
            UPDATE personal_info SET name=?, age=?, gender=?, height=?, weight=?, fitness_goal=?, activity_level=?
            WHERE id=?
        """, (name, age, gender, height, weight, fitness_goal, activity_level, session["user_id"]))
    else:
        db.execute("""
            INSERT INTO personal_info(id, name, age, gender, height, weight, fitness_goal, activity_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], name, age, gender, height, weight, fitness_goal, activity_level))
    db.commit()
    return redirect("/profile")

@app.route('/profile', methods=["GET"])
def profile():
    db = get_db()
    search = f"%{session['user_name']}%"
    names = db.execute("SELECT username FROM fees_paid WHERE username LIKE ?", (search,)).fetchall()
    data = db.execute("SELECT * FROM personal_info WHERE id = ?", (session["user_id"],)).fetchone()
    if not data:
        return redirect("/info")
    return render_template("profile.html", data=data, names=names)

workout_track = 0

@app.route('/workout_tracker', methods=["GET", "POST"])
def workout_tracker():
    global workout_track
    db = get_db()
    if request.method == "GET":
        return render_template("workout_tracker.html")
    workout_track += 1
    check = db.execute("SELECT user_id FROM number WHERE user_id = ?", (session["user_id"],)).fetchone()
    if check:
        current = db.execute("SELECT track FROM number WHERE user_id = ?", (session["user_id"],)).fetchone()["track"]
        db.execute("UPDATE number SET track = ? WHERE user_id = ?", (current + 1, session["user_id"]))
        track_data = current + 1
    else:
        db.execute("INSERT INTO number(user_id, track) VALUES (?, ?)", (session["user_id"], 1))
        track_data = 1

    sets = request.form.getlist("sets[]")
    reps = request.form.getlist("reps[]")
    weight = request.form.getlist("weight[]")
    exercise = request.form.getlist("exercise[]")
    today = request.form.get("date")

    if not sets or not reps or not weight:
        flash("Fill All Fields")
        return redirect("/workout_tracker")

    for i in range(len(sets)):
        db.execute("""
            INSERT INTO workout_logs (user_id, exercise, sets, reps, weight, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session["user_id"], exercise[i], sets[i], reps[i], weight[i], today))
    db.commit()
    return redirect("/dashboard")

@app.route('/workout_history', methods=["GET", "POST"])
def workout_history():
    db = get_db()
    history = db.execute("SELECT * FROM workout_logs WHERE user_id = ? ORDER BY date DESC", (session["user_id"],)).fetchall()
    return render_template("workout_history.html", history=history)

@app.route('/diet_Tracker', methods=["GET", "POST"])
def diet_tacker():
    return render_template("diet.html")

@app.route('/admin', methods=["GET", "POST"])
def admin():
    db = get_db()
    if request.method == "GET":
        return render_template("admin.html")
    paidlist = request.form.get("paidusers")
    db.execute("INSERT INTO fees_paid(username) VALUES (?)", (paidlist,))
    db.commit()
    return redirect("/feestatus")

@app.route('/feestatus', methods=["GET", "POST"])
def fee():
    db = get_db()
    name = db.execute("SELECT username FROM fees_paid").fetchall()
    return render_template("Feestatus.html", name=name)
