from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "secret"

CONFIG_PATH = "app/config.json"
LOG_PATH = "app/log.txt"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def login():
    config = load_config()
    if request.method == "POST":
        if request.form["username"] == config["username"] and request.form["password"] == config["password"]:
            session["login"] = True
            return redirect("/dashboard")
        return "用户名或密码错误"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("login"):
        return redirect("/")
    config = load_config()
    msg = ""
    if request.method == "POST":
        config["bearer_token"] = request.form["bearer_token"]
        config["serverchan_key"] = request.form["serverchan_key"]
        config["poll_interval"] = int(request.form["poll_interval"])
        config["twitter_users"] = [u.strip() for u in request.form["twitter_users"].split(",") if u.strip()]
        save_config(config)
        msg = "✅ 配置已保存"
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        logs = f.readlines()[-30:]
    return render_template("index.html", config=config, logs=logs, msg=msg)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
