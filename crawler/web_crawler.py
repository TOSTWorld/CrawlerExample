# -*- coding: utf-8 -*-
# @Author  : XieSiR
# @Time    : 2022/11/27 16:10
# @Function: a general templete crawler for webpage by mainly using beautiful soup
import sys
import time
import json
import requests
import random
from bs4 import BeautifulSoup


def str_reformat(s):
    if not isinstance(s, str):
        return ""
    s = s.replace('\n', '').replace('\r', '')
    s = s.strip()
    return s


# json_file_path example: templete.json; tmp/templete.json
def load_json_file(json_file_path):
    file = open(json_file_path, 'r', encoding='utf-8')
    return json.load(file)


def save_json_file(json_file_path, data):
    with open(json_file_path, 'w') as file_obj:
        json.dump(data, file_obj)


# WeChat notice
# get token via http://iyuu.cn/
def iyuu(token):
    url = f"https://iyuu.cn/{token}.send"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    def send(text):
        Form = {'text': text}
        return requests.post(url, data=Form, headers=headers, verify=False)

    return send


class WebCrawler:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.notify_wechat = iyuu(token)
        self.user_agent_list = \
            [
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
                ]
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'user-agent': ''
        }
        self.result = []

    def get_web_page_data(self, url):
        self.headers['user-agent'] = random.choice(self.user_agent_list)
        error_time = 0
        sleep_time = 2
        while True:
            try:
                r = requests.get(url=url, headers=self.headers)
                r.raise_for_status()
                if r.status_code == 200:
                    break
            except:
                print("Error while getting web page, sleep 2s")
                error_time += 1
                if error_time == 8:
                    self.notify_wechat("爬取不到网页达8次，已结束程序，快去看看~")
                    sys.exit()
                time.sleep(sleep_time)
                sleep_time *= 2
                continue
        soup = BeautifulSoup(r.text, 'html.parser')
        template = {
            "example": soup.find("div").string
        }
        return template

    def start(self):
        pass


if __name__ == '__main__':
    start_time = time.time()
    base_url = f'https://www.google.com/'
    token = '你自己的爱语飞飞的token'

    web_crawler = WebCrawler(base_url, token)
    web_crawler.get_web_page_data(base_url)
    end_time = time.time()
    print("task use time: " + str(end_time - start_time))
