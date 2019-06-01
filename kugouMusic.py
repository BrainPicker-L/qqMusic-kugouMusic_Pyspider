#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-05-30 11:47:48
# Project: zhutiqu_test1_kugou

from pyspider.libs.base_handler import *
import requests
import json
import re
import sys

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        page = 1
        count = 1
        while 1:
            url = "http://songsearch.kugou.com/song_search_v2?keyword=片尾曲&page={page}&pagesize=50&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0".format(
                page=page)
            r = requests.get(url=url, headers=headers)
            json_data = json.loads(r.content)
            song_list = json_data["data"]["lists"]
            if song_list == []:
                break
            else:
                song_type = u"片尾曲"

                for song in song_list:
                    song_from = song["Auxiliary"]
                    if song_from != "":
                        song_name1 = re.sub(r'<em>片尾曲</em>', '', song_from.encode('utf8'))
                        song_name2 = song["SongName"]
                        song_name = song_name2 + " " + song_name1
                        song_num = count
                        print
                        song_num, song_name, song_type
                        count += 1
                        self.crawl("http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=%s" % song["FileHash"],
                                   callback=self.index_page,
                                   save={'song_type': song_type, "song_name": song_name, "song_num": song_num})
            page += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        json_data = json.loads(response.content)
        song_url = json_data["url"]

        return {
            "song_url": song_url,
            'song_type': response.save["song_type"],
            "song_name": response.save["song_name"],
            "song_num": response.save["song_num"],
        }

