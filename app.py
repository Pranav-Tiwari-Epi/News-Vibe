import os
from flask import Flask,request
from flask_smorest import Api
from news import *
from models import db
app=Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"]=True # Poragate exceptions from extentions to main app
app.config['API_TITLE']='NEWS REST API'
app.config['API_VERSION']='v1' #Our version
app.config['OPENAPI_VERSION']='3.0.3'
app.config['OPENAPI_URL_PREFIX']='/'
#USE Swagger for API documentation
app.config['OPENAPI_SWAGGER_UI_PATH']='/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL']='https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:root@mysql_db:3306/news_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_NAME', 'news_db')
)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Rest of your configuration...


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api=Api(app)

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(frontend_bp, url_prefix='/')

