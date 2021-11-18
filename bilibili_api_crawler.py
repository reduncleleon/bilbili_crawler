import time
from bilibili_api import comment, sync, video, settings, Credential
import asyncio

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def dec(x):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor


def enc(x):
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''.join(r)


SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""


async def main():
    # 实例化 Credential 类
    # credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid="BV11q4y1G7cS")
    # 获取视频信息
    info = await v.get_info()
    display = [info['tname'], info['title'], info['duration'], info['owner']['mid'], \
               info['owner']['name'], info['stat']['view']]
    # 打印视频信息
    print(display)

    # 给视频点赞


# await v.like(True)


if __name__ == '__main__':
    # 主入口
    asyncio.get_event_loop().run_until_complete(main())
