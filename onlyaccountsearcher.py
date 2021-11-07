import requests
import time
import os

from notice import line_notice

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
LINE_TOKEN = os.getenv('LINE_TOKEN')


def get_followers(id):
    endpoint = "https://api.twitter.com/1.1/followers/ids.json"
    count = 5000
    params = {
        'user_id': id,
        'counts': count
    }
    header = {
        "Authorization": "Bearer {}".format(BEARER_TOKEN)
    }
    cursor = 1
    follower_list = []
    while cursor != 0:
        r = requests.get(endpoint, params=params, headers=header)
        try:
            r.raise_for_status()
        except Exception as e:
            print(e)
            remaining = int(r.headers['x-rate-limit-remaining'])
            limit_reset = int(r.headers['x-rate-limit-reset'])
        else:
            remaining = int(r.headers['x-rate-limit-remaining'])
            limit_reset = int(r.headers['x-rate-limit-reset'])
            l = r.json()["ids"]
            follower_list = follower_list + l
            cursor = r.json()["next_cursor"]
            params = {
                'user_id': id,
                'count': count,
                'cursor': cursor
            }
        finally:
            if remaining == 0:
                current_time =time.time()
                wait_time = limit_reset - current_time + 60
                time.sleep(wait_time)

    return follower_list    


def check_onlyaccount(id, follower=0, follow=1):
    endpoint = "https://api.twitter.com/1.1/users/show.json"
    follower_list = get_followers(id)

    for i in follower_list:
        params = {
        'user_id': i
        }
        header = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN)
            }
        r = requests.get(endpoint, params=params, headers=header)
        try:      
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if r.status_code in (420, 429):
                remaining = int(r.headers['x-rate-limit-remaining'])
                limit_reset = int(r.headers['x-rate-limit-reset'])
                current_time = time.time()
                wait_time = limit_reset - current_time + 5
                time.sleep(wait_time)
        else:
            follow = r.json()["friends_count"]
            follower = r.json()["followers_count"]
            screen_name = r.json()['screen_name']
            if follower == 0 and follow == 1:
                print(i)
                msg = '見つかりました。https://twitter.com/{}'.format(screen_name)
                try:
                    line_notice(LINE_TOKEN, msg)
                except Exception as e:
                        print(e)
        finally:
            remaining = int(r.headers['x-rate-limit-remaining'])
            if remaining == 0:
                limit_reset = int(r.headers['x-rate-limit-reset'])
                current_time =time.time()
                wait_time = limit_reset - current_time + 5
                time.sleep(wait_time)


def main(id):
    try:
        line_notice(LINE_TOKEN, "検索を開始します。")
    except Exception as e:
        print(e)

    check_onlyaccount(id)

    try:
        line_notice(LINE_TOKEN, "検索が終了しました。")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    id = os.getenv('TARGET_ID')
    main(id)