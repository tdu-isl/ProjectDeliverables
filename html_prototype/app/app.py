from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def top():
    return render_template("top.html")


@app.route("/shindan")
def shindan():
    return render_template("shindan_page.html")


@app.route("/shindan/result", methods=["POST"])
def result():
    field = request.form["field"]
    return render_template("shindan_result.html", message=field)


@app.route("/shindan/result/twitter_coop")
def twitter_coop():
    return render_template("twitter_coop.html")


if __name__ == "__main__":
    app.run(debug=True)
