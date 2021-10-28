import sqlite3

import xlwt
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import time
import numpy as np

def main():
    baseurl = r'https://www.bilibili.com/v/popular/rank/origin'
    datalist = getData(baseurl)
    save2Sqlite(datalist)
    print("爬取完毕！")



findLink = re.compile(r'<a class="title" href="//(.*?)"')
findLink_BV = re.compile(r'<a href="//www.bilibili.com/video/(.*?)"')
findTitle = re.compile(r'target="_blank">(.*?)</a>')
findPlay = re.compile(r'<i class="b-icon play"></i>(.*?)</span>',re.S)
findView = re.compile(r'<i class="b-icon view"></i>(.*?)</span>',re.S)
findAuthor = re.compile(r'<i class="b-icon author"></i>(.*?)</span>',re.S)

def getTime(select):
    if select == 0:
        return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
    else:
        return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
def getData(url):
    datalist = []
    html = askUrl(url)
    soup = BeautifulSoup(html, "html.parser")
    i = 1

    for item in soup.find_all('li',class_="rank-item"):
        data = []
        item = str(item)

        link = re.findall(findLink,item)[0]
        data.append(link)

        link_BV = re.findall(findLink_BV,item)[0]
        data.append(link_BV)

        title = re.findall(findTitle,item)[1]  #第二条才是标题信息
        data.append(title)

        play = re.findall(findPlay,item)[0]
        play = re.sub(r"\n?","",play)
        play = play.strip()
        data.append(play)

        view = re.findall(findView,item)[0]
        view = re.sub(r'\n?',"",view)
        view = view.strip()
        data.append(view)

        author = re.findall(findAuthor, item)[0]
        author = re.sub(r'\n?', "", author)
        author = author.strip()
        data.append(author)

        datalist.append(data)
        # print("title="+title,end=" ")
        # print("play="+play,end=" ")
        # print("view="+view,end=" ")
        # print(link)
    return datalist

def askUrl(url):
    head = {
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        # "Cookie": "LIVE_BUVID=AUTO7616141634535512; _uuid=04246967-129B-6F76-1A91-EE69108D331253842infoc; buvid3=172471DD-E77B-49CC-A9D6-2DD52B0FB0CA18546infoc; sid=asoxcr51; buvid_fp=172471DD-E77B-49CC-A9D6-2DD52B0FB0CA18546infoc; DedeUserID=13251505; DedeUserID__ckMd5=41cb4ff0a0df1c54; SESSDATA=cd2dbcd1%2C1629715528%2C3d32e*21; bili_jct=b47ee00b3f332e6f0be9d94422c9706e; bsource=search_baidu; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(ku|J|YkYRk0J'uYkkJY|RkJ; bp_t_offset_13251505=530554660080301534; PVID=1; bp_video_offset_13251505=531209792922976972; fingerprint3=5f1cc142f58e5770207c4f1bb945c045; fingerprint=900cd9e21a26b9f8aa07323b9c87a733; fingerprint_s=26d0b0f4626f1baf1d3346c2531395f0; buvid_fp_plain=172471DD-E77B-49CC-A9D6-2DD52B0FB0CA18546infoc",
        # "Host": "www.bilibili.com",
        # "Referer": "https://www.bilibili.com/",
        # "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        # "sec-ch-ua-mobile": "?0",
        # "Sec-Fetch-Dest": "document",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "same-origin",
        # "Sec-Fetch-User": "?1",
        # "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }
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

# def saveData(datalist):
#     book = xlwt.Workbook(encoding="uft-8",style_compression=0)#不允许改变表格样式
#     sheet = book.add_sheet("bilibili热门视频排行榜",cell_overwrite_ok=True)#允许单元格覆写
#     col = ["视频链接","BV号","标题","播放量","评论","作者"]
#     sheet.write(0,0,"爬取时间")
#     sheet.write(0,1,getTime(0))
#     for i in range(0,len(col)):
#         sheet.write(1,i,col[i])
#     for i in range(0,100):
#         data = datalist[i]
#         for j in range(0,len(data)):
#             sheet.write(i+2,j,data[j])
#     bookName = "bili_ranking_"+getTime(1)+".xlsx"
#     savepath = "./output/" + bookName
#     book.save(savepath)
def save2Sqlite(datalist):
    conn = sqlite3.connect('data.db')
    conn.execute("""
      create table if not exists bilibili_rank_video(
      bvid varchar prinmary key,
      title varchar DEFAULT NULL,
      comment_num int DEFAULT NULL,
      author varchar DEFAULT NULL)""")

    command = "insert into bilibili_rank_video \
                 values(?,?,?,?);"
    result = np.array(datalist)
    result = np.delete(result, [0,3], axis=1)

    for row in result:
        try:
            conn.execute(command, row)
        except Exception as e:
            print(e)
            conn.rollback()
    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()