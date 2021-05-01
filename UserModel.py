from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from setting import Base
from setting import ENGINE


#動画のインスタンス
class videoInfo(Base):
    __tablename__ = 'videoInfo'
    id = Column(String(20), primary_key=True)
    title = Column(String(50))
    channel = Column(String(30))
    description=Column(String(500))
    viewCount = Column(Integer)
    videoURL = Column(String(200))
    imageURL = Column(String(200))
    kind = Column(String(20))

    def __init__(self,id,title,channel,description,viewCount,videoURL,imageURL,kind):
        self.id=id
        self.title=title
        self.channel=channel
        self.description=description
        self.viewCount=viewCount
        self.videoURL=videoURL
        self.imageURL=imageURL
        self.kind=kind
    
    def __repr__(self):
        return "id:"+self.id+"タイトル:"+self.title+",チャンネル名:"+self.channel+",概要欄:"+self.description+",再生数:"+str(self.viewCount)+",URL:"+self.videoURL+",サムネ:"+self.imageURL+",動画サイト名:"+self.kind
    

  

if __name__ == "__main__":
    Base.metadata.create_all(bind=ENGINE)