from flask import Flask, render_template, request
import requests


app = Flask(__name__)


def init():
    global SITEKEY, SECRETKEY
    global ADMITTED_MSG, DENIED_MSG

    with open(".sitekey", mode="r") as f:
        SITEKEY = f.read()
    with open(".secretkey", mode="r") as f:
        SECRETKEY = f.read()

    ADMITTED_MSG = "認証に成功しました。"
    DENIED_MSG = {
        "invalid-input-response": "認証に失敗しました。\nトークンが無効または不正です。",
        "bad-request": "認証に失敗しました。\nリクエストが無効または不正です。",
        "timeout-or-duplicate": "認証に失敗しました。\nトークンが古すぎるか、すでに使われています。",
        "unknown": "認証に失敗しました。"
    }

    app.run(port=8080, host="localhost", debug=True)


@app.route("/", methods=["POST", "GET"])
def index():
    challenge_result = None
    print(request.form.get("g-recaptcha-response", None))
    if request.form.get("g-recaptcha-response", None) is not None:
        url = "https://www.google.com/recaptcha/api/siteverify"
        body = {
            "secret": SECRETKEY,
            "response": request.form.get("g-recaptcha-response")
        }
        resp = requests.post(url, data=body)
        print(resp.status_code)
        if resp.status_code == requests.codes.ok:
            if resp.json()["success"]:
                challenge_result = ADMITTED_MSG
            else:
                challenge_result = DENIED_MSG.get(resp.json()["error-codes"][0], DENIED_MSG["unknown"])

    return render_template("index.html", sitekey=SITEKEY, secretkey=SECRETKEY, challenge_result=challenge_result, showup=challenge_result is not None)


@app.route("/detail")
def detail():
    return render_template("detail.html")


@app.route("/add")
def add():
    return render_template("add.html")


if __name__ == "__main__":
    init()
