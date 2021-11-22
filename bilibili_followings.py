import time
import threading
import sqlite3
import requests
import json
from concurrent import futures


result = []
lock = threading.Lock()
total = 1
conn = None
cookie = {'domain': '/',
          'expires': 'false',
          'httpOnly': 'false',
          'name': 'buvid3',
          'path': 'Fri, 29 Jan 2021 08:50:10 GMT',
          'value': '7A29BBDE-VA94D-4F66-QC63-D9CB8568D84331045infoc,bilibili.com'}

uas = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'


def create():
    # 创建数据库
    global conn
    conn = sqlite3.connect('data.db')
    conn.execute("""
    create table if not exists bilibili_followings(
    id int prinmary key autocrement ,
    mid int DEFAULT NULL,
    mname varchar DEFAULT NULL,
    uid int DEFAULT NULL,
    uname varchar DEFAULT NULL)""")


def run(url):
    # 启动爬虫
    global total, result, uas, cookie
    mid = url.replace('https://space.bilibili.com/', '')
    mid = int(mid.replace('/fans/follow', ''))
    head = {'User-Agent': uas,
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'http://space.bilibili.com',
            'Host': 'm.bilibili.com',
            'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': url}
    time.sleep(1)  # 延迟，避免太快 ip 被封
    try:
        url = 'http://api.bilibili.com/x/relation/followings?vmid=' + str(mid)
        html = requests.get(url, headers=head, cookies=cookie, timeout=10).text
        j = json.loads(html)

        followings = j['data']['list']
        for item in followings:
            following = (total, mid, 'mname', item['mid'], item['uname'])
            result.append(following)
            print(following)
            total += 1
    except Exception as e:
        # print(e)
        return
    with lock:
        print(total)


def save():
    # 将数据保存至本地
    global result, conn, flag, total
    command = "insert into bilibili_followings values(?, ?, ?, ?, ?);"
    for row in result:
        try:
            conn.execute(command, row)
        except Exception as e:
            print(e, row[0], row[1])
    conn.commit()
    result = []


if __name__ == "__main__":
    create()
    total_num = 1000000
    num = 500
    for i in range(20, int(total_num / num)):
        begin = num * i
        urls = ["https://space.bilibili.com/{}/fans/follow".format(j)
                for j in range(begin, begin + num)]
        with futures.ThreadPoolExecutor(10) as executor:
            executor.map(run, urls)
        save()
    conn.close()
