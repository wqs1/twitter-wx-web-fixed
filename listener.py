import time, json, os
import tweepy, requests

CONFIG_FILE = "config.json"
LOG_FILE = "listener.log"

def log(text):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()}: {text}\n")
    print(text)

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

last_ids = {}

def run():
    while True:
        config = load_config()
        if not config["bearer_token"] or not config["twitter_users"]:
            log("未配置必要信息")
            time.sleep(30)
            continue
        try:
            client = tweepy.Client(bearer_token=config["bearer_token"])
            for user in config["twitter_users"]:
                user = user.strip()
                user_info = client.get_user(username=user)
                if not user_info or not user_info.data: continue
                user_id = user_info.data.id
                tweets = client.get_users_tweets(id=user_id, max_results=5)
                if tweets and tweets.data:
                    latest = tweets.data[0]
                    if last_ids.get(user) != latest.id:
                        last_ids[user] = latest.id
                        text = latest.text
                        url = f"https://twitter.com/{user}/status/{latest.id}"
                        msg = f"{user} 有新推文:\n\n{text}\n\n👉 {url}"
                        send_wechat(config["serverchan_key"], msg)
                        log(f"推送：{url}")
        except Exception as e:
            log(f"错误：{e}")
        time.sleep(config.get("poll_interval", 60))

def send_wechat(key, text):
    if not key: return
    url = f"https://sctapi.ftqq.com/{key}.send"
    requests.post(url, data={"title": "Twitter 通知", "desp": text})

if __name__ == "__main__":
    run()
