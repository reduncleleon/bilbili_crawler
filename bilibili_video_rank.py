import sqlite3
import re
import urllib.request
import urllib.error
import time
import numpy as np
from bs4 import BeautifulSoup

findLink = re.compile(r'<a class="title" href="//(.*?)"')
findLink_BV = re.compile(r'<a href="//www.bilibili.com/video/(.*?)"')
findTitle = re.compile(r'target="_blank">(.*?)</a>')
findPlay = re.compile(r'<i class="b-icon play"></i>(.*?)</span>', re.S)
findView = re.compile(r'<i class="b-icon view"></i>(.*?)</span>', re.S)
findAuthor = re.compile(r'<i class="b-icon author"></i>(.*?)</span>', re.S)


def main():
    parts = ['all', 'music', 'dance', 'game', 'douga', 'knowledge',
             'tech', 'sports', 'car', 'life', 'food', 'animal',
             'kichiku', 'fashion', 'ent', 'cinephile', 'origin', 'rookie']

    for part in parts:
        baseurl = r'https://www.bilibili.com/v/popular/rank/' + part
        datalist = get_data(baseurl)
        save2Sqlite(datalist)
    print("爬取完毕！")


def get_time(select):
    if select == 0:
        return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
    else:
        return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())


def get_data(url):
    datalist = []
    html = ask_url(url)
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all('li', class_="rank-item"):
        data = []
        item = str(item)

        link = re.findall(findLink, item)[0]
        data.append(link)

        link_BV = re.findall(findLink_BV, item)[0]
        data.append(link_BV)

        title = re.findall(findTitle, item)[1]  # 第二条才是标题信息
        data.append(title)

        play = re.findall(findPlay, item)[0]
        play = re.sub(r'\n?', "", play)
        play = play.strip()
        data.append(play)

        view = re.findall(findView, item)[0]
        view = re.sub(r'\n?', "", view)
        view = view.strip()
        data.append(view)

        author = re.findall(findAuthor, item)[0]
        author = re.sub(r'\n?', "", author)
        author = author.strip()
        data.append(author)

        datalist.append(data)
    return datalist


def ask_url(url):
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.77 Safari/537.36"}

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def save2Sqlite(datalist):
    conn = sqlite3.connect('data.db')
    conn.execute("""
      create table if not exists bilibili_rank_video(
      bvid varchar prinmary key,
      title varchar DEFAULT NULL,
      comment_num int DEFAULT NULL,
      author varchar DEFAULT NULL)""")

    command = "insert into bilibili_rank_video values(?, ?, ?, ?);"
    result = np.array(datalist)
    result = np.delete(result, [0, 3], axis=1)

    for row in result:
        try:
            conn.execute(command, row)
            print(row)
        except Exception as e:
            print(e)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
