import requests
import os
import json
import datetime
import urllib
from typing import Dict

"""
Explore how to make all the queries work. Here are most of the API support links
https://developer.twitter.com/en/docs/twitter-api/conversation-id
https://developer.twitter.com/en/docs/tutorials/getting-historical-tweets-using-the-full-archive-search-endpoint
https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query <- very helpful!
https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters
https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all#Optional
https://developer.twitter.com/en/docs/twitter-api/tweets/counts/introduction
"""

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = "AAAAAAAAAAAAAAAAAAAAAMVPWAEAAAAAo3uC%2Fq68qUXLTwi41%2FKxXCvsYVI%3DAXG4U2nYO73pvhag3stPFPli4aR9VFYsxAa3bbTN2DW9OU40fL"
#bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = os.environ.get("BEARER_TOKEN_2")

# https://api.twitter.com/2/tweets/counts/all?query=from%3ATwitterDev&start_time=2021-05-01T00:00:00Z&end_time=2021-06-01T00:00:00Z&granularity=day
def create_counts_url(query:str, start_time:str, end_time:str, granularity:str = "day", next_token:str = None):
    url = "https://api.twitter.com/2/tweets/counts/all?query={}&start_time={}&end_time={}&granularity={}".format(
        query, start_time, end_time, granularity)
    if next_token != None:
        url = "{}&next_token={}".format(url, next_token)
    print("create_counts_url(): {}".format(url))
    return url

# 'https://api.twitter.com/2/tweets/search/all?query=from:twitterdev&max_results=500'
def create_historical_url(query:str, max_result:int = 10, time_str:str = None, next_token:str = None) -> str:
    tweet_fields = "tweet.fields=lang,author_id,in_reply_to_user_id,created_at,conversation_id"
    url = "https://api.twitter.com/2/tweets/search/all?max_results={}&query={}&{}".format(max_result, query, tweet_fields)
    if time_str != None:
        url = "{}&{}".format(url, time_str)
    if next_token != None:
        url = "{}&next_token={}".format(url, next_token)
    print("max_result = {}\nurl = {}".format(max_result, url))
    return url

def create_recent_conversation_url(conversation_id:str) -> str:
    conversation_id = "1484131517878181891"
    tweet_fields = "tweet.fields=lang,author_id,in_reply_to_user_id,created_at,conversation_id"
    url = "https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{}&{}".format(conversation_id, tweet_fields)
    print(url)
    return url

def create_tweets_url(tweet_ids:str) -> str:
    tweet_fields = "tweet.fields=lang,author_id,conversation_id,created_at"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    #ids = "ids=1278747501642657792,1255542774432063488"
    # ids = "ids=1484131517878181891"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?ids={}&{}".format(tweet_ids, tweet_fields)
    print(url)
    return url

def create_keywords_url(query:str, max_result:int = 10, time_str:str = None, next_token:str = None) -> str:
    tweet_fields = "tweet.fields=lang,author_id,in_reply_to_user_id,created_at"
    url = "https://api.twitter.com/2/tweets/search/all?max_results={}&query={}&{}".format(max_result, query, tweet_fields)
    if time_str != None:
        url = "{}&{}".format(url, time_str)
    if next_token != None:
        url = "{}&next_token={}".format(url, next_token)
    print("max_result = {}\nurl = {}".format(max_result, url))
    return url



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url) -> json:
    response = requests.request("GET", url, auth=bearer_oauth)
    print("Status code = : {}".format(response.status_code))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def print_response(title:str, j:json):
    json_str = json.dumps(j, indent=4, sort_keys=True)
    print("\n------------ Begin '{}':\nresponse:\n{}\n------------ End '{}'\n".format(title, json_str, title))

def tweet_id_query_example():
    url = create_tweets_url("1484131517878181891")
    url = create_tweets_url("1531844023459008512")
    json_response = connect_to_endpoint(url)
    print_response("Get tweet", json_response)

def historical_query_example():
    query = "from:philfeld" # "to:philfeld and is:reply"
    query = '"china virus"' # "to:philfeld and is:reply"
    timeframe = "end_time=2018-07-18T00:00:00.000Z"
    timeframe = "start_time=2022-06-01T00:00:00.000Z&end_time=2022-06-02T00:00:00.000Z"
    url = create_historical_url(query=query, time_str=timeframe, max_result=10)
    json_response = connect_to_endpoint(url)
    print_response("Get historical conversation", json_response)

def tweet_keyword_time_query_example(query:str = "aaaa bbbb"):
    print("tweet_keyword_time_query_example")
    query = '"china virus"  place_country:US lang:en'
    date_str = "2022-06-05T00:00:00Z"
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    print("dt = {}".format(dt.strftime("%B %d %Y %H:%M")))
    url = create_keywords_url(query)
    json_response = connect_to_endpoint(url)
    print_response("Get keyword tweets", json_response)


def counts_query_example():
    query = "from:twitterdev"
    query = "chinavirus"
    start_time = "2020-01-01T00:00:00Z"
    end_time = "2021-01-01T00:00:00Z"
    url = create_counts_url(query, start_time, end_time)
    json_response = connect_to_endpoint(url)
    print_response("Get counts", json_response)

    meta:Dict = json_response['meta']
    count:int = 2
    while 'next_token' in meta:
        next_token = meta['next_token']
        url = create_counts_url(query, start_time, end_time, next_token=next_token)
        json_response = connect_to_endpoint(url)
        print_response("Get counts {}".format(count), json_response)
        meta = json_response['meta']
        count += 1

def main():
    print("BEARER_TOKEN = {}".format(bearer_token))

    tweet_id_query_example()
    # url = create_recent_conversation_url("1484131517878181891")
    # json_response = connect_to_endpoint(url)
    # print_response("Get recent conversation", json_response)
    # historical_query_example()
    # counts_query_example()

    #tweet_keyword_time_query_example()




if __name__ == "__main__":
    main()