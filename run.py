import sys
import os
from requests import get
from requests.exceptions import ConnectTimeout, ReadTimeout


def get_id_url(name, token):
    return "https://api.vk.com/method/users.get?user_ids=" + name + "&v=5.74&access_token=" + token


def get_friends_url(id, token):
    return "https://api.vk.com/method/friends.get?user_id=" + str(id) +\
           "&fields=nickname&v=5.74&access_token=" + token


def get_friends(json):
    return "\n".join((" ".join((str(t["id"]), t["first_name"], t["last_name"]))
                      for t in json["response"]["items"]))


def get_info(name, get_url_func, json_to_result):
    try:
        token = os.environ["MY_VK_TOKEN"]
        id_json = get(get_id_url(name, token)).json()
        if 'response' not in id_json:
            print("User not found.")
        else:
            friends_json = get(get_url_func(id_json['response'][0]['id'], token)).json()
            print(json_to_result(friends_json))
    except (ConnectTimeout, ReadTimeout):
        print("Connection timeout.")


if __name__ == '__main__':
    get_info(sys.argv[1], get_friends_url, get_friends)
