import time

import matplotlib
import wordcloud
import sqlite3
from bilibili_api import comment, sync , video, settings,Credential
import asyncio

async def main():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute("select bvid from bilibili_rank_video limit 0,1000 ")
    for it in cursor:
        bid = ''.join(it)
        try:
            # 获取视频信息
            v = video.Video(bvid=bid)
            info = await v.get_info()
            display = [info['tname'], info['title'], info['duration'], info['owner']['mid'], \
                       info['owner']['name'], info['stat']['view']]
            # 打印视频信息
            print(display)
            time.sleep(0.1)
        except Exception as e:
            print(e)


    conn.close()
if __name__ == '__main__':
    # 主入口
    asyncio.get_event_loop().run_until_complete(main())