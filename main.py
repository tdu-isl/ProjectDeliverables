from flask import Flask, request, render_template, redirect
from UserModel import videoInfo
from setting import session
from sqlalchemy import *
from sqlalchemy import desc
from sqlalchemy.orm import *
import json
import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname
import re
from datetime import datetime, timedelta

video = []


# インスタンス化し、videoリストに入れる(nico)
def nico_res(word):
    # 動画情報取得
    url = "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
    # クエリパラメータの設定
    params = {'q': word,
              'targets': 'title,tags',
              'fields': 'title,description,contentId,thumbnailUrl,viewCounter,lengthSeconds,startTime',
              '_sort': '-viewCounter',
              '_context': 'apiguide',
              '_limit': '10'
              }

    req = requests.get(url, params=params)
    res = json.loads(req.text)

    # 各種パラメータを取得する関数
    def getId(i):
        return res["data"][i]["contentId"]

    def getTitle(i):
        return res["data"][i]["title"]

    def getChannel(i):
        chaUrl = "https://ext.nicovideo.jp/api/getthumbinfo/" + res["data"][i]["contentId"]
        chareq = requests.get(chaUrl)
        if (res["data"][i]["contentId"].find("nm") == -1) and (res["data"][i]["contentId"].find("sm") == -1):
            channel = chareq.text[chareq.text.find('<ch_name>') + 9:chareq.text.find('</ch_name>')]

        else:
            channel = chareq.text[chareq.text.find('<user_nickname>') + 15:chareq.text.find('</user_nickname>')]
        return channel

    def getDescription(i):
        description = res["data"][i]["description"].replace("<br />", "").replace("<br>", "").replace("</span>",
                                                                                                      "").replace(
            "<span style=\"color: #000000; font-size: 13px;\">", "")
        return description

    def getViewCounter(i):
        return res["data"][i]["viewCounter"]

    def getVideoURL(i):
        return "https://nico.ms/" + res["data"][i]["contentId"]

    def getImageURL(i):
        return res["data"][i]["thumbnailUrl"]

    def getPostTime(i):
        return res["data"][i]["startTime"]

    def getPlayTime(i):
        return res["data"][i]["lengthSeconds"]

    for i in range(len(res["data"])):
        resvideo = videoInfo(getId(i), getTitle(i), getChannel(i), getDescription(i), getViewCounter(i), getVideoURL(i),
                             getImageURL(i), getPostTime(i), getPlayTime(i), "ニコニコ動画")
        # print(resvideo)
        video.append(resvideo)


# インスタンス化し、videoリストに入れる(Youtube)
def you_res(word):
    # YoutubeAPIキーはセキュリティ対策のため.envファイル(ローカルに保存)からロード
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # 動画情報取得
    url = "https://www.googleapis.com/youtube/v3/search"
    # クエリパラメータの設定
    params = {'type': 'video',
              'part': 'snippet',
              'q': word,
              'key': os.environ.get("Youtube_API_KEY"),
              'maxResults': '1',
              'regionCode': 'jp',
              'fields': 'items(id(videoId),snippet(title,description,channelTitle,publishedAt,thumbnails(high(url))))'
              }

    req = requests.get(url, params=params)
    res = json.loads(req.text)

    # 各種パラメータを取得する関数
    def getId(i):
        return res["items"][i]["id"]["videoId"]

    def getTitle(i):
        return res["items"][i]["snippet"]["title"]

    def getChannel(i):
        return res["items"][i]["snippet"]["channelTitle"]

    def getDescription(i):
        return res["items"][i]["snippet"]["description"]

    def getViewCounter(resVideoInfoAPI):
        return resVideoInfoAPI["items"][0]["statistics"]["viewCount"]

    def getVideoURL(i):
        return "https://www.youtube.com/watch?v=" + res["items"][i]["id"]["videoId"]

    def getImageURL(i):
        return res["items"][i]["snippet"]["thumbnails"]["high"]["url"]

    def getPostTime(i):
        return res["items"][i]["snippet"]["publishedAt"]

    # YoutubeData(video)APIを1動画ごとに取得する
    def getVideoInfo(i):
        counturl = "https://www.googleapis.com/youtube/v3/videos"
        params2 = {'part': 'statistics,contentDetails',
                   'id': res["items"][i]["id"]["videoId"],
                   'key': os.environ.get("Youtube_API_KEY"),
                   'fields': 'items(statistics(viewCount),contentDetails(duration))'
                   }
        req = requests.get(counturl, params=params2)
        return json.loads(req.text)

    def getPlayTime(resVideoInfoAPI):
        return pt2sec(resVideoInfoAPI["items"][0]["contentDetails"]["duration"])

    def pt2sec(pt_time):
        pttn_time = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')
        keys = ['hours', 'minutes', 'seconds']
        m = pttn_time.search(pt_time)
        kwargs = {k: 0 if v is None else int(v[:-1])
                  for k, v in zip(keys, m.groups())}
        sec = int(timedelta(**kwargs).total_seconds())
        return sec

    for i in range(len(res["items"])):
        resVideoInfoAPI = getVideoInfo(i)
        resvideo = videoInfo(getId(i), getTitle(i), getChannel(i),
                             getDescription(i), getViewCounter(resVideoInfoAPI),
                             getVideoURL(i), getImageURL(i),
                             getPostTime(i), getPlayTime(resVideoInfoAPI), "Youtube")
        # print(resvideo)
        video.append(resvideo)


def video_sort(sort):
    # 再生数少ない方から
    if sort == "asc_videoCount":
        db_videoInfo = session.query(videoInfo).order_by(videoInfo.viewCount).all()
    # 再生数多いい方から
    elif sort == "des_videoCount":
        db_videoInfo = session.query(videoInfo).order_by(desc(videoInfo.viewCount)).all()
    # 再生時間少ない方から
    elif sort == "asc_playTime":
        db_videoInfo = session.query(videoInfo).order_by(videoInfo.playTime).all()
    # 再生時間多いい方から
    elif sort == "des_playTime":
        db_videoInfo = session.query(videoInfo).order_by(desc(videoInfo.playTime)).all()
    # 投稿日時早い順(古い)から
    elif sort == "asc_postTime":
        db_videoInfo = session.query(videoInfo).order_by(videoInfo.postTime).all()
    # 投稿日時遅い順(新しい)から
    elif sort == "des_postTime":
        db_videoInfo = session.query(videoInfo).order_by(desc(videoInfo.postTime)).all()
    return db_videoInfo


# appという名前でFlaskのインスタンスを作成
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


# 登録処理
@app.route('/', methods=["POST"])
def register_record():
    word = request.form.get("word")

    # ニコニコ動画
    nico_res(word)
    # you_res(word)
    for i in range(len(video)):
        new_video = videoInfo(id=video[i].id, title=video[i].title, channel=video[i].channel,
                              description=video[i].description, viewCount=video[i].viewCount,
                              videoURL=video[i].videoURL, imageURL=video[i].imageURL, postTime=video[i].postTime,
                              playTime=video[i].playTime, kind=video[i].kind)
        session.add(new_video)

    session.commit()

    # databaseをリスト型で取得

    sort = request.form.get("sortPattern")
    alert = ""

    if sort:
        # alert = "並び替えを行いました。"
        if sort == "asc_videoCount":
            alert = "再生数が少ない順に並び替えました。"

        # 再生数多いい方から
        elif sort == "des_videoCount":
            alert = "再生数が多い順に並び替えました。"

        # 再生時間少ない方から
        elif sort == "asc_playTime":
            alert = "再生時間が短い順に並び替えました。"

        # 再生時間多いい方から
        elif sort == "des_playTime":
            alert = "再生時間が長い順に並び替えました。"

        # 投稿日時早い順(古い)から
        elif sort == "asc_postTime":
            alert = "投稿日時が早い順に並び替えました。"

        # 投稿日時遅い順(新しい)から
        elif sort == "des_postTime":
            alert = "投稿日時が遅い順に並び替えました。"

        db_videoInfo = video_sort(sort)
    else:
        db_videoInfo = session.query(videoInfo).all()

    """
    #ソートのkeyを持ってくる
    sort = request.form.get("sort")
    
    〇video_sort関数を作ったので以下のように使用
    db_videoInfo=video_sort(sort)

    sortに入れる文字列は
    #再生数少ない方から　"asc_videoCount"
    #再生数多いい方から　"des_videoCount"
    #再生時間少ない方から　"asc_playTime"
    #再生時間多いい方から　"des_playTime"
    #投稿日時早い順(古い)から　"asc_postTime"
    #投稿日時遅い順(新しい)から　"des_postTime"
    の6つのパターン
    """

    # 既存のDBは次の検索の為に削除
    session.query(videoInfo).delete()
    session.commit()
    video.clear()

    return render_template('index2.html', db_videoInfo=db_videoInfo, word=word, alert=alert)


# return redirect("/")


# 取得処理
@app.route('/index2')
def index2():
    # databaseをリスト型で取得
    db_videoInfo = session.query(videoInfo).all()

    # 既存のDBは次の検索の為に削除
    session.query(videoInfo).delete()
    session.commit()
    video.clear()

    return render_template('index2.html', db_videoInfo=db_videoInfo)


if __name__ == '__main__':
    app.debug = True
    app.run()

"""
# appという名前でFlaskのインスタンスを作成
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

# 登録処理
@app.route('/', methods=["POST"])
def register_record():
    word = request.form.get("word")

    # ニコニコ動画
    nico_res(word)
    you_res(word)
    for i in range(len(video)):
        new_video = videoInfo(id=video[i].id, title=video[i].title, channel=video[i].channel,
                              description=video[i].description, viewCount=video[i].viewCount,
                              videoURL=video[i].videoURL, imageURL=video[i].imageURL,
                              postTime=video[i].postTime, playTime=video[i].playTime,
                              kind=video[i].kind)
        session.add(new_video)

    session.commit()
    return redirect("/")


# 取得処理
@app.route('/index2')
def index2():
    # databaseをリスト型で取得
    db_videoInfo = session.query(videoInfo).all()
    # 既存のDBは次の検索の為に削除
    session.query(videoInfo).delete()
    session.commit()
    video.clear()

    return render_template('index2.html', db_videoInfo=db_videoInfo)


if __name__ == '__main__':
    app.debug = True
    app.run()
"""
