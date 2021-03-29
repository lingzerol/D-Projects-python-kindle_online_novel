from flask import Flask, render_template, request, jsonify, redirect, url_for
from utils import tools

app = Flask(__name__)
cookie_pool = tools.CookiePool()
password = "300303"


def check_cookie():
    if request.headers.has_key("Cookie"):
        cookie = request.headers.get("Cookie")
        return cookie_pool.check(cookie)
    return False


@app.route("/")
def root():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    input_passwd = request.form.get("password")
    input_passwd = tools.decrypt(input_passwd)
    if input_passwd == password:
        cookie = tools.create_cookie({"name": "zero"})
        cookie_pool.add(cookie)
        return {"message": "success!", "cookie": cookie}
    else:
        return {"message": "fail!"}


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/cookie", methods=["POST"])
def cookie():
    if check_cookie():
        return {"message": "success!"}
    return {"message": "fail!"}

@app.route("/content")
def content():
    return render_template('content.html')

@app.route("/menu")
def menu():
    return render_template('menu.html')

@app.route("/shelf")
def shelf():
    return render_template('shelf.html')


if __name__ == "__main__":
    app.run(port=8081, debug=True)
