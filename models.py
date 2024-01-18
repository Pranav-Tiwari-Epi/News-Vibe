from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class NewsModel(db.Model):
    __tablename__="news_analysis"

    index=db.Column(db.Integer,primary_key=True)
    source=db.Column(db.String)
    author=db.Column(db.String)
    url=db.Column(db.String)
    time=db.Column(db.Time)
    date=db.Column(db.Date)
    title=db.Column(db.String)
    analysisContent=db.Column(db.String)
    sentimentAnalysis=db.Column(db.String)
    