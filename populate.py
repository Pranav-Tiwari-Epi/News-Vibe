#!/usr/bin/env python
# coding: utf-8
import time
import numpy as np
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
import mysql.connector
import os

# Fetch data from the API
url = 'https://newsapi.org/v2/everything?q=+India+Maldives&searchIn=title&language=en&apiKey=f04ce8be72f0475093faa83c0b60ea39'
headers = {'Accept': 'application/json'}
req = requests.get(url, headers=headers)

# Check if the request was successful
if req.status_code == 200:
    api_response = req.json()

    # Create a DataFrame from API response
    response_df = pd.DataFrame(api_response['articles'])
    df = response_df.copy(deep=True)

    # Data preprocessing steps
    df['source'] = df['source'].apply(lambda x: x['name'])
    df = df.drop(['urlToImage'], axis=1)
    df['date'] = pd.to_datetime(df['publishedAt']).dt.date
    df['time'] = pd.to_datetime(df['publishedAt']).dt.time
    df = df.drop('publishedAt', axis=1)
    df = df.dropna()
    
    def analysis_text(text):
        first2line = text.split('.')[0:2]
        first2line = ''.join(first2line)
        if len(first2line) >= 200:
            return first2line[:200]
        return first2line
    
    df['Analysis Content'] = df['description'].apply(analysis_text)
    df = df.drop(['content', 'description'], axis=1)

    def apply_filter(content):
        if 'deleted' in content and ('content' in content or 'post' in content):
            print(content)
            return np.nan
        return content

    df['Analysis Content'] = df['Analysis Content'].apply(lambda x: apply_filter(x))
    df = df.dropna()

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    def sentiment_analysis(text):
        comp_score = analyzer.polarity_scores(text)['compound']
        if comp_score >= .25:
            return 'Pos'
        elif comp_score >= -.25:
            return 'Neutral'
        else:
            return 'Neg'
    
    df['Sentiment Analysis'] = df['Analysis Content'].apply(lambda x: sentiment_analysis(x))
    # # Connect to MySQL database
    try:
        # Define MySQL connection parameters for SQLAlchemy
        hostname = os.getenv('DB_HOST', 'localhost')
        database = os.getenv('DB_NAME', 'news_db')
        username = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', '')
        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(
    host=hostname, db=database, user=username, pw=password
        ))

        
        df = df.rename(columns={'Sentiment Analysis': 'sentimentAnalysis', 'Analysis Content': 'analysisContent'})
        
        df.to_sql(con=engine, name='news_analysis', if_exists='replace', index=True)
        
    except mysql.connector.Error as err:
        print("An error occurred:", err)
else:
    print("Failed to fetch data from the API. HTTP Status Code:", req.status_code)