import json
import time
import tweepy
import requests
import os

CONFIG_PATH = "app/config.json"
LOG_PATH = "app/log.txt"

def log(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def send_wechat(text, key):
    url = f"https://sctapi.ftqq.com/{key}.send"
    data = {"title": "推特通知", "desp": text}
    requests.post(url, data=data)

def main():
    last_tweet_ids = {}
    while True:
        try:
            config = load_config()
            client = tweepy.Client(bearer_token=config["bearer_token"])
            for username in config["twitter_users"]:
                user = client.get_user(username=username)
                if not user or not user.data:
                    log(f"用户未找到: {username}")
                    continue
                user_id = user.data.id
                tweets = client.get_users_tweets(id=user_id, max_results=5)
                if tweets and tweets.data:
                    latest = tweets.data[0]
                    tweet_id = latest.id
                    if last_tweet_ids.get(username) != tweet_id:
                        last_tweet_ids[username] = tweet_id
                        text = f"{username} 有新推文:\n\n{latest.text}\n\n👉 https://twitter.com/{username}/status/{tweet_id}"
                        send_wechat(text, config["serverchan_key"])
                        log(f"已推送: {username}")
            time.sleep(config["poll_interval"])
        except Exception as e:
            log(f"错误: {e}")
            time.sleep(10)

if __name__ == "__main__":
    log("启动监听器")
    main()
