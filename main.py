from flask import Flask, request, render_template , redirect
from UserModel import videoInfo
from setting import session
from sqlalchemy import *
from sqlalchemy.orm import *
import json
from bs4 import BeautifulSoup
import requests

video = []
#インスタンス化し、videoリストに入れる(nico)
def nico_res(url):
    req = requests.get(url)
    res = json.loads(req.text)
    
    for i in range(len(res["data"])):
            chaUrl = "https://ext.nicovideo.jp/api/getthumbinfo/"+res["data"][i]["contentId"]
            chareq = requests.get(chaUrl)
            res["data"][i]["description"] = res["data"][i]["description"].replace("<br />","")
            resvideo = videoInfo(res["data"][i]["contentId"],res["data"][i]["title"],chareq.text[chareq.text.find('<user_nickname>')+15:chareq.text.find('</user_nickname>')],res["data"][i]["description"],res["data"][i]["viewCounter"],"https://nico.ms/"+res["data"][i]["contentId"],res["data"][i]["thumbnailUrl"],"ニコニコ動画")
            video.append(resvideo)

#インスタンス化し、videoリストに入れる(Youtube)
def you_res(word):
    # 動画情報取得
    url = "https://www.googleapis.com/youtube/v3/search"
    # パラメータの設定
    params = {'type': 'video',
            'part': 'snippet',
            'q': word,
             'key': 'AIzaSyDP1Ya1uZetxtl4D4lkbHR5MY-xPpGvVE8',
            'maxResults': '1',
            'regionCode': 'jp',
             'fields': 'items(id(videoId),snippet(title,description,channelTitle,thumbnails(high(url))))'
             }

    req = requests.get(url, params=params)
    res = json.loads(req.text)

    # 視聴回数取得
    counturl = "https://www.googleapis.com/youtube/v3/videos"
    
    for i in range(len(res["items"])):
            # パラメータの設定
            params2 = {'part': 'statistics',
                    'id': res["items"][i]["id"]["videoId"],
                    'key': 'AIzaSyDP1Ya1uZetxtl4D4lkbHR5MY-xPpGvVE8',
                    'fields': 'items(statistics(viewCount))'
            }
            resvideo = videoInfo(res["items"][i]["id"]["videoId"],res["items"][i]["snippet"]["title"],res["items"][i]["snippet"]["channelTitle"],res["items"][i]["snippet"]["description"],json.loads(requests.get(counturl, params=params2).text)["items"][0]["statistics"]["viewCount"],"https://www.youtube.com/watch?v="+res["items"][i]["id"]["videoId"],res["items"][i]["snippet"]["thumbnails"]["high"]["url"],"Youtube")
            video.append(resvideo)



# appという名前でFlaskのインスタンスを作成
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


# 登録処理
@app.route('/', methods=["POST"])
def register_record():
   
    word = request.form.get("word")
    session.query(videoInfo).delete()
    
    #ニコニコ動画
    nicoURL= "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search?q="+word+"&targets=title,tags&fields=title,description,contentId,thumbnailUrl,viewCounter&_sort=-viewCounter&_context=apiguide,_limit=10"
    nico_res(nicoURL)
    you_res(word)
    for i in range(len(video)):
        new_video = videoInfo(id=video[i].id , title=video[i].title, channel=video[i].channel, description=video[i].description , viewCount=video[i].viewCount , videoURL=video[i].videoURL , imageURL=video[i].imageURL , kind=video[i].kind)
        session.add(new_video)  
    

    session.commit()
    return redirect("/")

# 取得処理
@app.route('/', methods=["GET"])
def fetch_record():
    db_videoInfo = session.query(videoInfo).all()
    

    #return render_template("index.html", name=name, message=message)


if __name__ == '__main__':
    app.run()
