import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'xxx'

# 在q後面打入我想要的關鍵字
search_url = "https://api.twitter.com/1.1/search/tweets.json?q=Electricity+costs+in+Norway"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'tweet_mode':'extended'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    content = json.dumps(json_response, indent=4,
                         sort_keys=True)
    print(content)
    with open('elonmusk.json', 'w', encoding='utf8') as json_file:
        json.dump(json_response, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
