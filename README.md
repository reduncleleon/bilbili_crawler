# bilbili_crawler

（有点菜，bilibili_user暂时还跑不起来，各位大佬可以fork后一起调一下）<br>
* 代码功能：
  * bilibili_video_rank:爬取排行榜热门视频，一次100条，可通过修改专栏url爬取新视频
  * analyser：利用上述获得的BV号，获取更加详细的播放量、up主及标签等信息
  * Calcu_Sim:使用词向量处理计算词相似度，将过多的标签量聚类成有限的标签个数，更加便于展示和分析
  * Figure：使用pyecharts展示分析统计图表
