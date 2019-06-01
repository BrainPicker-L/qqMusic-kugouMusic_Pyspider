#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-05-30 09:52:01
# Project: zhutiqu_test1

from pyspider.libs.base_handler import *
import requests
import json
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
class Handler(BaseHandler):
    crawl_config = {
        'headers':{
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        page = 1
        count = 1
        while 1:
            url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p={page}&n=1000&w=片尾曲'.format(page=page)
            r = requests.get(url=url,headers=headers)
            json_data = json.loads(r.content[9:-1])
            song_list = json_data["data"]["song"]["list"]
            if song_list == []:
                break
            else:

                print(len(song_list))
                for song in song_list:
                    if "片尾曲" in song["lyric"]:
                        song_type = song["lyric"][-3:]
                        song_name = "%s %s"%(song["songname"],song["lyric"][:-3])
                        song_num = count
                        song_mid = song["songmid"]
                        count += 1
                        self.crawl("https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?format=json205361747&platform=yqq&cid=205361747&songmid=%s&filename=C400%s.m4a&guid=126548448"%(song_mid,song_mid),callback=self.index_page,save= {'song_type':song_type,"song_name":song_name,"song_num":song_num,"song_mid":song_mid})

                page += 1
    def index_page(self,response):
        print(response.save)
        json_data = json.loads(response.content)
        vkey = json_data["data"]["items"][0]["vkey"]
        print(response.save["song_mid"])
        song_url = "http://ws.stream.qqmusic.qq.com/C400%s.m4a?fromtag=0&guid=126548448&vkey=%s"%(response.save["song_mid"],vkey)
        return {
            "song_url": song_url,
            'song_type':response.save["song_type"],
            "song_name":response.save["song_name"],
            "song_num":response.save["song_num"],
        }
