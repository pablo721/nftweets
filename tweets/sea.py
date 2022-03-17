import pandas as pd
import requests
import json


def sea_collections():
    url = 'https://api.opensea.io/api/v1/collections?offset=0&limit=300'
    headers = {'Accept': 'application/json', 'limit': '3500'}
    df = pd.DataFrame(json.loads(requests.request('GET', url, headers=headers).text)['collections'])
    stats_df = df['stats']
    return df.drop('stats', axis=1), stats_df

def sea_assets():
    url = "https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=20"
    headers = {"Accept": "application/json", "X-API-KEY": "5bec8ae0372044cab1bef0d866c98618"}
    return requests.request("GET", url, headers=headers).text


def sea_events():
    url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=20"
    headers = {"Accept": "application/json", "X-API-KEY": "5bec8ae0372044cab1bef0d866c98618"}
    return requests.request("GET", url, headers=headers).text


def sea_bundles():
    url = "https://api.opensea.io/api/v1/bundles?limit=20&offset=0"
    return requests.request("GET", url).text


def sea_collection_stats(name):
    url = f"https://api.opensea.io/api/v1/collection/{name}/stats"
    headers = {"Accept": "application/json"}
    return requests.request("GET", url, headers=headers).text


def sea_asset(address):
    url = f"https://api.opensea.io/api/v1/asset/{address}/1/"
    return requests.request("GET", url).text


def sea_contract(address):
    url = f"https://api.opensea.io/api/v1/asset_contract/{address}"
    return requests.request("GET", url).text

