#!/usr/bin/env python3
from flask import Flask, request, Response, flash, render_template, redirect, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from datetime import datetime
from collections import defaultdict
import requests
import urllib
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password


# ログイン用ユーザー作成
users = {
    #"mizoguchi": User(1, "mizoguchi", "18fi112"),
    #"sai": User(2, "sai", "18fi055"),
    #"morohashi": User(3, "morohashi", "17fi097"),
    #"ikuta": User(4, "ikuta", "18fi008")
}


@login_manager.user_loader
def load_user(user_id):
    for u in users.values():
        if(str(u.id) == user_id):
            return u
        else:
            print('not found this user in dict')


@app.route('/')
def home():
    return redirect('/login')


# ログインしないと表示されないパス
@app.route('/home', methods=["GET", "POST"])
@login_required
def protected():
    if(request.method == "GET"):
        print("GET ~~~")
        return render_template("home.html", user=current_user.name, orders=None)
    
    if(request.method == "POST"):
        print("POST ~~~")
        token = request.cookies.get(current_user.name + '_token', None)
        if(token == None):
            return Response(">>> Failed to get token from cookie")
        print("access_token:")
        print(token)
        
        url = 'http://127.0.0.1:8008/orders/' + current_user.name
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        responseFromAPI = requests.post(url=url, headers=headers, cookies=request.cookies)
        orders = json.loads(responseFromAPI.content)
        
        return render_template("home.html", user=current_user.name, orders=orders)


# ログインパス
@app.route('/login', methods=["GET", "POST"])
def test():
    if(request.method == "GET"):
        return render_template("login.html")
    
    if(request.method == "POST"):
        user_name = request.form.get('username')
        user_pass = request.form.get('password')
        url = 'http://127.0.0.1:8008/token'
        params = {
            'username': user_name,
            'password': user_pass,
        }
        params = urllib.parse.urlencode(params)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        responseFromAPI = requests.post(url=url, data=params, headers=headers)
        
        if(responseFromAPI.status_code == 200):
            
            if user_name not in users:
                print('add user: ' + user_name)
                users[user_name] = User(len(users)+1, user_name, user_pass)
            
            tokens = json.loads(responseFromAPI.text)  # 'access_token', 'refresh_token', 'token_type'
            login_user(users.get(user_name))
            print("access_token:")
            print(tokens["access_token"])
            print("refresh_token:")
            print(tokens["refresh_token"])

            
            response = make_response(redirect('/home'))
            max_age = 60 * 60 * 24 # 24h
            expires = int(datetime.now().timestamp()) + max_age
            response.set_cookie(
                user_name + '_token',
                value=tokens['access_token'],
                max_age=max_age,
                expires=expires,
                path='/',
                secure=None,
                httponly=False
            )
            
            return response
        else:
            flash("認証失敗しました", "failed")
            return render_template("login.html")


# ログアウトパス
@app.route('/logout')
@login_required
def logout():
    response = make_response(redirect('/login'))
    response.delete_cookie(current_user.name + '_token')
    logout_user()
    return response


if __name__ == '__main__':
    import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(
        'ssl/fullchain1.pem', 'ssl/privkey1.pem'
    )
    app.run(host="0.0.0.0",port=8000,debug=True, ssl_context=ssl_context)
