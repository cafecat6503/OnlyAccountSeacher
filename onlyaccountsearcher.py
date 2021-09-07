import requests
import time
import os

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm'
LINE_TOKEN = os.getenv('LINETOKEN')


def get_followers(id):
    endpoint = "https://api.twitter.com/1.1/followers/ids.json"
    count = 5000
    params = {
        'user_id': id,
        'count': count
    }
    header = {
        "Authorization": "Bearer {}".format(BEARER_TOKEN)
    }

    r = requests.get(endpoint, params=params, headers=header)
    r.raise_for_status()

    follower_list = r.json()["ids"]
    cursor = r.json()["next_cursor"]
    while cursor != 0:
        params = {
            'user_id': id,
            'count': count,
            'cursor': cursor
        }
        r = requests.get(endpoint, params=params, headers=header)
        l = r.json()["ids"]
        cursor = r.json()["next_cursor"]
        follower_list = follower_list + l

    return follower_list


def check_onlyaccount(id):
    endpoint = "https://api.twitter.com/1.1/users/show.json"
    params = {
        'user_id': id
    }
    header = {
        "Authorization": "Bearer {}".format(BEARER_TOKEN)
    }
    r = requests.get(endpoint, params=params, headers=header)
    r.raise_for_status()
    
    follow = r.json()["friends_count"]
    follower = r.json()["followers_count"]

    if follower == 0 and follow == 1:
        return True
    else:
        return False


def search_onlyaccount(id):
    follower_list = get_followers(id)

    for i in follower_list:
        try:
            result = check_onlyaccount(i)
        except Exception as e:
            print(e)
        else:
            if result:
                print(i)
        finally:
            time.sleep(1.01)


def line_notice(token):
    endpoint = "https://notify-api.line.me/api/notify"
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    msg = {
        "message" :  "検索が終了しました。"
        }
    r = requests.post(endpoint, headers = header, params=msg)
    r.raise_for_status()


def main(id):
    search_onlyaccount(id)
    try:
        line_notice(LINE_TOKEN)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    id = os.getenv('TARGET_ID')
    main(id)