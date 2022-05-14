from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def shindan():
    return render_template("shindan_page.html")

@app.route("/result", methods=["POST"])
def result():
    field = request.form["field"]
    return render_template("shindan_result.html", message = field)

@app.route("/result/twitter_coop")
def twitter_coop():
    return render_template("twitter_coop.html")

if __name__ == "__main__":
    app.run(debug=True)