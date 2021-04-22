from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from setting import Base
from setting import ENGINE


#動画のインスタンス
class videoInfo(BASE):
    __tablename__ = 'videoInfo'
    id = Column(String, primary_key=True, autoincrement=True)
    title = Column(String)
    channel = Column(String)
    viewCount = Column(Integer)
    videoUrl = Column(String)
    imageUrl = Column(String)

    def __init__(self,title,channel,viewCount,videoUrl,imageUrl):
        self.title=title
        self.channel=channel
        self.viewCount=viewCount
        self.videowUrl=videoUrl
        self.imageUrl=imageUrlS
    
  

if __name__ == "__main__":
    Base.metadata.create_all(bind=ENGINE)