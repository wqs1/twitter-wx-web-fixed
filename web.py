from flask import Flask, render_template_string, request, redirect, url_for, session
import json, os, subprocess

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 请更换为强密码
CONFIG_FILE = "config.json"
LOG_FILE = "listener.log"
USERNAME = "admin"
PASSWORD = "123456"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect("/config")
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/config")
    return render_template_string(LOGIN_PAGE)

@app.route("/config", methods=["GET", "POST"])
def config():
    if not session.get("logged_in"):
        return redirect("/")
    config = load_config()
    if request.method == "POST":
        config["bearer_token"] = request.form["bearer_token"]
        config["serverchan_key"] = request.form["serverchan_key"]
        config["poll_interval"] = int(request.form["poll_interval"])
        config["twitter_users"] = request.form["twitter_users"].split(",")
        save_config(config)
    return render_template_string(CONFIG_PAGE, config=config)

@app.route("/start")
def start_listener():
    if not session.get("logged_in"):
        return redirect("/")
    subprocess.call(["supervisorctl", "start", "listener"])
    return redirect("/config")

@app.route("/stop")
def stop_listener():
    if not session.get("logged_in"):
        return redirect("/")
    subprocess.call(["supervisorctl", "stop", "listener"])
    return redirect("/config")

@app.route("/logs")
def logs():
    if not session.get("logged_in"):
        return redirect("/")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = f.read()[-5000:]
    else:
        log = "暂无日志"
    return f"<pre>{log}</pre>"

LOGIN_PAGE = """
<h2>登录系统</h2>
<form method='post'>
  用户名：<input name='username'><br>
  密码：<input type='password' name='password'><br>
  <input type='submit' value='登录'>
</form>
"""

CONFIG_PAGE = """
<h2>Twitter 自动转发系统</h2>
<form method="post">
  Bearer Token:<br>
  <input name="bearer_token" value="{{config.bearer_token}}" size="60"><br><br>
  Server酱 Key:<br>
  <input name="serverchan_key" value="{{config.serverchan_key}}" size="40"><br><br>
  监听用户（逗号分隔）:<br>
  <input name="twitter_users" value="{{",".join(config.twitter_users)}}" size="50"><br><br>
  轮询间隔（秒）:<br>
  <input name="poll_interval" value="{{config.poll_interval}}"><br><br>
  <input type="submit" value="保存配置">
</form><br>
<a href='/start'>▶ 启动监听</a> |
<a href='/stop'>⏹ 停止监听</a> |
<a href='/logs'>📜 查看日志</a> |
<a href='/'>🔒 登出</a>
"""

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
