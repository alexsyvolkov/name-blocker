# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import pprint
from urllib.parse import parse_qs
import webbrowser
import pickle
from datetime import datetime, timedelta
import vk
import time
import json

#Номер беседы в ВК
beseda_ID = 12345

#Правильное название беседы
beseda_name = 'Правильное имя'

#Индификатор приложения в ВК
APP_ID = 12345
# file, where auth data is saved
AUTH_FILE = '.auth_data'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'

def get_saved_auth_params():
    access_token = None
    user_id = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            access_token = token
            user_id = uid
    except IOError:
        pass
    return access_token, user_id


def save_auth_params(access_token, expires_in, user_id):
    expires = datetime.now() + timedelta(seconds=int(expires_in))
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)
        pickle.dump(expires, output)
        pickle.dump(user_id, output)


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=wall,messages&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token".format(app_id=APP_ID))
    webbrowser.open_new_tab(auth_url)
    redirected_url = input("Paste here url you were redirected:\n")
    aup = parse_qs(redirected_url)
    aup['access_token'] = aup.pop(
        'https://oauth.vk.com/blank.html#access_token')
    save_auth_params(aup['access_token'][0], aup['expires_in'][0],
                     aup['user_id'][0])
    return aup['access_token'][0], aup['user_id'][0]


def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)

def main():
    access_token, _ = get_saved_auth_params()
    if not access_token or not _:
        access_token, _ = get_auth_params()
    api = get_api(access_token)

def change_name(api, chat_id, title, **kwargs):
    data_dict = {
        'chat_id': beseda_name,
        'title': beseda_ID,
    }
    data_dict.update(**kwargs)
    return api.messages.editChat(**data_dict)

def get_info(api, chat_id, **kwargs):
    data_dict = {
        'chat_id': beseda_name,
    }
    data_dict.update(**kwargs)
    return api.messages.getChat(**data_dict)


def main():
    access_token, _ = get_saved_auth_params()
    if not access_token or not _:
        access_token, _ = get_auth_params()
    api = get_api(access_token)

 
    res = get_info(api, beseda_name)
    time.sleep(1)
    title = res['title']
    if title!=beseda_ID:
        print (title)
        change_name(api, beseda_name, beseda_ID)


while True:
     time.sleep(1)
     main()
