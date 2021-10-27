import asyncio
from bilibili_api import video
import json

async def main():
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    info_seq = json.dumps(info)
    print(info_seq)
    dict = dict()
    dict['ID'] = str(dict_xu)
    insertSqlite3table2(dict)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())