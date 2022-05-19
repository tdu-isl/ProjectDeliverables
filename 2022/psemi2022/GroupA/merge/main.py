from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    with open(".sitekey", mode="r") as f:
        sitekey = f.read()
    with open(".secretkey", mode="r") as f:
        secretkey = f.read()

    print(request.form.get("g-recaptcha-response", "None"))
    if request.form.get("g-recaptcha-response", None) is not None:
        url = "https://www.google.com/recaptcha/api/siteverify"
        body = {
            "secret": secretkey,
            "response": request.form.get("g-recaptcha-response")
        }
        print(requests.post(url, data=body).json())

    return render_template("index.html", sitekey=sitekey, secretkey=secretkey)

@app.route("/detail",methods=["POST", "GET"])
def detail():
    return render_template("detail.html")

# @app.route("/test")
# def _index():
#     with open(".sitekey", mode="r") as f:
#         sitekey = f.read()
#     with open(".secretkey", mode="r") as f:
#         secretkey = f.read()

#     return render_template("_index.html", sitekey=sitekey, secretkey=secretkey)


if __name__ == "__main__":
    app.run(port=8080, host="localhost", debug=True)
