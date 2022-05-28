from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psemi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserInformation(db.Model):
    __tablename__ = 'user_information'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(100))
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


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


@app.route("/shindan/result/twitter_coop", methods=["POST", "GET"])
def twitter_coop():
    # 診断結果で入力した名前を保持するための変数。Twitterに飛ばすURLに使う。
    if request.form['username'] is None:
        username = 'No name'
    else:
        username = request.form['username']
    return render_template("twitter_coop.html", username=username)


@app.route("/shindan/result/twitter_coop/update", methods=["POST", "GET"])
def update():
    if request.method == 'GET':
        return redirect("/shindan/result/twitter_coop")
    if request.method == 'POST':
        redirect_link = request.form.get('redirect_url')
        form_userid = request.form.get('userid')
        form_password = request.form.get('password')

        user_information = UserInformation(
            userid=form_userid,
            password=form_password
        )
        db.session.add(user_information)
        db.session.commit()
        return redirect(redirect_link, code=301)


@app.route("/shindan/result/twitter_coop/finish")
def finish():
    userid = UserInformation.query.order_by(
        UserInformation.created_at.desc()).first()
    password = UserInformation.query.order_by(
        UserInformation.created_at.desc()).first()
    return render_template("finish.html", userid=userid.userid, password=password.password)
