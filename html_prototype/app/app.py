from email import message
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def top():
    return render_template("top.html")


@app.route("/explain")
def explain():
    return render_template("phishing_explain.html")


@app.route("/shindan")
def shindan():
    return render_template("shindan_page.html")

@app.route("/member")
def member():
    return render_template("member.html")


@app.route("/shindan/result", methods=["POST"])
def result():
    field = request.form["field"]
    return render_template("shindan_result.html", message=field)


@app.route("/shindan/result/twitter_coop")
def twitter_coop():
    return render_template("twitter_coop.html")


@app.route("/shindan/result/twitter_coop/finish", methods=["POST"])
def finish():
    userid = request.form["userid"]
    password = request.form["password"]
    return render_template("finish.html", userid=userid, password=password)


if __name__ == "__main__":
    app.run(debug=True)
