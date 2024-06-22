import requests
import json
import base64

def get_header():
    url = "http://192.168.122.113/wp-json/wp/v2"

    user = "streamverse_admin"
    password = "KmBs eLm4 8dlW 0nw2 v4dl Jg9y"

    creds = user + ":" + password

    token = base64.b64encode(creds.encode())

    header = {"Authorization": 'Basic ' + token.decode('utf-8')}

    return header, url


def check_for_duplicate_post(url, header, service, title, year):
    post_title = f'{title} | {service} | {year}'

    # Search for posts that match the title, service, and year
    params = {
        'search': post_title,
        'per_page': 1,
    }
    r = requests.get(url + '/posts', headers=header, params=params)
    posts = r.json()

    if len(posts) > 0:
        return True
    else:
        return False


def post_content(url, header, service, title, image_url, year):
    if check_for_duplicate_post(url, header, service, title, year) == False:
        post = {
            'title': f'{title} | {service} | {year}',
            'content': f" <img src=\"{image_url}\" alt=\"External Image\" />",
            'status': "publish",
        }
        r = requests.post(url + '/posts',headers=header, json=post)
        print(r)


