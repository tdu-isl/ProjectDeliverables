from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from setting import Base
from setting import ENGINE


# 動画のインスタンス
class videoInfo(Base):
    __tablename__ = 'videoInfo'
    id = Column(String(20), primary_key=True)
    title = Column(String(50))
    channel = Column(String(30))
    description = Column(String(500))
    viewCount = Column(Integer)
    videoURL = Column(String(200))
    imageURL = Column(String(200))
    postTime = Column(TIMESTAMP)
    playTime = Column(Integer)
    kind = Column(String(20))

    def __init__(self, id, title, channel, description, viewCount, videoURL, imageURL, postTime, playTime, kind):
        self.id = id
        self.title = title
        self.channel = channel
        self.description = description
        self.viewCount = viewCount
        self.videoURL = videoURL
        self.imageURL = imageURL
        self.postTime = postTime
        self.playTime = playTime
        self.kind = kind

    def __repr__(self):
        return "id:" + self.id + \
               ",タイトル:" + self.title + \
               ",\nチャンネル名:" + self.channel + \
               ",\n概要欄:" + self.description + \
               ",\n再生数:" + str(self.viewCount) + \
               ",\nURL:" + self.videoURL + \
               ",\nサムネ:" + self.imageURL + \
               ",\n投稿日時:" + self.postTime + \
               ",\n再生時間:" + str(self.playTime) + \
               ",\n動画サイト名:" + self.kind


if __name__ == "__main__":
    Base.metadata.create_all(bind=ENGINE)
