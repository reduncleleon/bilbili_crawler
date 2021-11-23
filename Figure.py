from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
import time
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.execute("select tag, count(tag) as num from video_info group by tag")
kind = []
kind_num = []
for it in cursor:
    kind.append(it[0])
    kind_num.append(it[1])

conn.commit()
conn.close()

kind_simple = ['MV','舞蹈' ,'健身', '影视','音乐', '生活' ,'动物', '手办' ,'数码' ,'鬼畜' ,'搞笑' ,'汽车'
       , '游戏' , '体育' ,'知识' ,'穿搭' ,'美食' ,'计算机']
KindMap = {'GMV': 'MV', 'MAD·AMV': '鬼畜', 'MMD·3D': '数码', 'MV': 'MV', 'VOCALOID·UTAU': '音乐', '中国舞': '舞蹈', '人力VOCALOID': '生活', '人文历史': '生活', '健身': '健身', '动物综合': '动物', '单机游戏': '游戏', '原创音乐': '音乐', '喵星人': '鬼畜', '国产原创相关': '影视', '大熊猫': '动物', '娱乐杂谈': '搞笑', '宅舞': '舞蹈', '家居房产': 'MV', '工业·工程·机械': '数码', '影视剪辑': '数码', '影视杂谈': '影视', '手办·模玩': '手办', '手工': '手办', '手机游戏': '游戏', '搞笑': '搞笑', '摩托车': '汽车', '数码': '数码', '日常': '生活', '时尚潮流': '穿搭', '明星综合': '数码', '明星舞蹈': '舞蹈', '智能出行': '数码', '极客DIY': '手办', '校园学习': '知识', '桌游棋牌': '游戏', '汪星人': '鬼畜', '汽车文化': '汽车', '汽车极客': '汽车', '汽车生活': '汽车', '演奏': '游戏', '热点': '手办', '爬宠': '手办', '特摄': '影视', '环球': '生活', '田园美食': '美食', '电子竞技': '游戏', '电音': '数码', '短片': '影视', '短片·手书·配音': '影视', '社会': '生活', '社科·法律·心理': '生活', '科学科普': '知识', '穿搭': '穿搭', '竞技体育': '体育', '篮球·足球': '体育', '粉丝创作': '游戏', '绘画': '影视', '综合': '数码', '综艺': '影视', '网络游戏': '游戏', '美妆护肤': '穿搭', '美食侦探': '美食', '美食制作': '美食', '美食测评': '美食', '美食记录': '美食', '翻唱': '手办', '职业职场': '生活', '舞蹈教程': '舞蹈', '舞蹈综合': '舞蹈', '街舞': '舞蹈', '计算机技术': '计算机', '设计·创意': '穿搭', '财经商业': '生活', '购车攻略': '汽车', '软件应用': '数码', '运动文化': '舞蹈', '运动综合': '体育', '野生动物': '动物', '野生技能协会': '动物', '音MAD': '音乐', '音乐现场': '音乐', '音乐综合': '音乐', '音游': '音乐', '预告 资讯': '知识', '鬼畜剧场': '鬼畜', '鬼畜调教': '鬼畜'}

#简化类别后重新统计标签数目
kind_num_simple = {}.fromkeys(kind_simple, 0)
for i in range(len(kind)):
    kind_num_simple[KindMap.get(kind[i])] += kind_num[i]

data_pairs = [list(z) for z in zip(kind, kind_num)]
data_pairs.sort(key=lambda x: x[1])

data_pairs_simple = [list(z) for z in zip(kind_num_simple.keys(), kind_num_simple.values())]
data_pairs_simple.sort(key=lambda x: x[1])


c = (
    Pie()
    .add(
        "",
        data_pair=data_pairs,
        center=["77%", "60%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="热门视频标签饼状图",pos_left='80%'),
        legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),)
    .render("pie_tag.html")
)
c = (
    Pie()
    .add(
        "",
        data_pair=data_pairs_simple,
        center='center',
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="分类后热门视频标签饼状图",pos_left='30%'),
        legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),)
    .render("pie_tag_simple.html")
)

c = (
    WordCloud()
    .add("", data_pairs, word_size_range=[12, 55],mask_image='icon.png')
    .set_global_opts(title_opts=opts.TitleOpts(title="B站热门视频标签词云",pos_left="center"))
    .render("wordcloud_tag.html")
)