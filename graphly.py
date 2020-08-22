import tweepy
from tweepy import Cursor,API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler,Stream
consumerKey = '8cjnT2jmrxu350Fy3M2a0kUx4'
consumerSecret = 'sA2B2cD0FxSUjoGkpqlJRrshySGdgF8buZCZIrjpmQ6tN8HWMB'
accessToken = '1083684732099940352-iEw1jzLPWldBDrpc1PJ4kwoyBEDP2Z'
accessTokenSecret = 'aC9hWhLXkOttnDZUFYxgLi7Y3q953vkvUFsGAqPSXeyz0'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api=API(auth,wait_on_rate_limit=True)

for tweet in tweepy.Cursor(api.search,q="IndiaChinaFaceOff",lang='en',count=1000,since='2020-06-15',tweet_mode="extended").items(4000):
    date=tweet._json['created_at']
    print(date)
    with open('tweetCur.json','ab') as file:
        file.write(str(str(tweet._json)+'\n').encode('utf-8'))
import pandas as pd

data=pd.read_csv('location.csv')
print(data.columns)
data=data[['country','city_ascii','iso3']]
print(data)
data.to_csv('city_country_data.csv')
import json


def string_to_json(line):
    import ast
    jsonval = ast.literal_eval(line)
    return jsonval


location = []
for line in open('tweetCur.json', 'r', encoding="utf-8"):
    line = string_to_json(line)
    print(line['user']['name'])
    # print(line.keys())
    if line['user']['location']:
        print(line['user']['location'])
        location.append(line['user']['location'])

for l in location:
    with open('location.txt', 'a') as w:
        try:
            w.write(l + '\n')
        except:
            continue
import pandas as pd
import numpy as np
import tqdm
data=pd.read_csv('city_country_data.csv')
df=pd.DataFrame(columns=['Country','code'])
with open('location.txt','r')as r:
    location=r.readlines()

for i in tqdm.tqdm(data['country'].unique()):
    for j in location:
        if i is not np.NAN:
            if i.lower() in j.lower():
                del(location[location.index(j)])
                coun=data.loc[data['country']==i,['country','iso3']]
                df.loc[-1] = coun.iloc[0].values # adding a row
                df.index = df.index + 1
for i in tqdm.tqdm(data['city_ascii']):
    if i == np.NAN or isinstance(i,float):
        pass
    else:
        for j in location:
            if i.lower() in j.lower():
                del (location[location.index(j)])
                coun = data.loc[data['city_ascii'] == i, ['country', 'iso3']]
                df.loc[-1] = coun.iloc[0].values  # adding a row
                df.index = df.index + 1
df.to_csv('tweet_location.csv')

import pandas as pd
import plotly.offline as py

df = pd.read_csv('tweet_location.csv')
count_dict=dict(df['Country'].value_counts())
df['count']=df['Country'].map(count_dict)
df=df.drop(['Unnamed: 0'],axis=1)
df=df.drop_duplicates()
print(df)

data = [ dict(
        type = 'choropleth',showscale=True,autocolorscale=True,locations=df['Country'],text = df['Country'],z=df['count'],locationmode='country names')]

py.plot(data)