import requests


def line_notice(token, message):
    endpoint = "https://notify-api.line.me/api/notify"
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    params = {
        "message" :  message
        }
    r = requests.post(endpoint, headers = header, params=params)
    r.raise_for_status()