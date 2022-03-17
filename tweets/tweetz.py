import pandas as pd
import numpy as np
import requests
import os
import json
import datetime
import ccxt
from .models import NFT, TwitterAcc

count_interval = 3.2
lookup_interval = 1.2
search_interval = 2.2

bearer_token = os.environ.get("BEARER_TOKEN")

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_uids(file='../data/user_ids.csv'):
    usernames = pd.read_csv(file, index_col=0).index.values
    usernames_str = ','.join(usernames)
    multi_link = f'https://api.twitter.com/2/users/by?usernames={usernames_str}'
    json_response = connect_to_endpoint(multi_link, {})
    df = pd.DataFrame(data={'id': 0}, index=usernames, dtype='int64')
    for user in json_response['data']:
        try:
            df.loc[user['username'], 'id'] = user['id']
        except:
            pass
    return df


def get_users_tweets(username, user_id=None, max_results=100):
    if not user_id:
        user_id = TwitterAcc.objects.get(username=username).user_id
    tweets_url = f'https://api.twitter.com/2/users/{user_id}/tweets'
    json_response = connect_to_endpoint(tweets_url, {'max_results': max_results})
    return pd.DataFrame(json_response['data'])


def tweet_count(keyword, interval='minute'):
    query_params = {'query': keyword, 'granularity': interval}
    count_url = "https://api.twitter.com/2/tweets/counts/recent"
    json_response = connect_to_endpoint(count_url, query_params)
    df = pd.DataFrame(json_response['data'])
    df = df[['start', 'end', 'tweet_count']]
    #since = ccxt.Exchange.parse8601(df.loc[0, 'start'])
    df[['start', 'end']] = df[['start', 'end']].applymap(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M'))
    return df


def get_spaces(users):
    users = ','.join(users)
    spaces_link = f'https://api.twitter.com/2/spaces/by/creator_ids?user_ids={users}'
    json_response = connect_to_endpoint(spaces_link, {})
    return pd.DataFrame(json_response['data'])


def popular_tweets():
    tweets = []
    for acc in TwitterAcc.objects.all():
        his_tweets = get_users_tweets(username=acc.username, user_id=acc.user_id)
        tweets.append(his_tweets)

    print(tweets)


