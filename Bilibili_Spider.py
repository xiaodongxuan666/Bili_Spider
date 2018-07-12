
# coding: utf-8
# Writer: Mike_Shine
# Date: 2018-7-11

# 这段代码是输入B站UP主的编号（User_Mid------进入up主的主页 https://space.bilibili.com/91236407/#/video。 其中91236407即为 User_Mid），然后爬取主页内的视频（
# 有一点没有做的就是说这段代码只爬100个。如果想要爬所有的视频，你可以

import json
import re
import os
import requests

# 从主页拿视频列表的函数
def get_Mainpage_Video(User_Mid):

    headers = {
    'Host': 'space.bilibili.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'https://space.bilibili.com/' + str(User_Mid)+ '/',    # 这里是Mid
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid='+ str(User_Mid)+'&pagesize=100&tid=0&page=1&keyword=&order=pubdate'
    # 请求 Url 前面要加上   主机地址！  在这里就是space.xxxxxx   
    # 注意从浏览器里抓包可以看到完整的地址，而从Fiddler
    #最大的请求size是100
    
    content = requests.get(url, headers = headers, verify = False).json()
    i = content['data']['count'] # 视频个数
    video_List=[]
    for num in range(i):
        aid =  content['data']['vlist'][num]['aid']
        title = content['data']['vlist'][num]['title']
        author = content['data']['vlist'][num]['author']
        tmp = {"aid":aid,"title":title,"author":author}
        video_List.append(tmp)
    print("Up猪:" + str(video_List[0]["author"]) + "本次共有" + str(i) + "个视频")
    return video_List 


#  拿下载视频的Url
def get_video_url(video_List):
    video_url = []
    # 每个视频地址都进去网页，拿到下载参数：url 
    for i in range(len(video_List)):
        url = 'https://www.bilibili.com/video/av'+ str(video_List[i]['aid'])      # 每个的Url
        html = requests.get(url, verify = False).text
        url_patn = re.compile(r'"url":"(.*?)","backup_url"')
        video_url.append(re.findall(url_patn, html)[0])
    return video_url



# 用拿到的视频列表和视频Url来下载视频
def download(video_url, video_list):
    path = r"D:/video/" + video_list[0]['author']+ "/"
    if not os.path.isdir(path):
        os.makedirs(path)
    for i in range(len(video_list)):
        headers = {
        'Host': 'data.bilibili.com', 
        'Connection': 'keep-alive',
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.bilibili.com/video/av'+ str(video_list[i]['aid'])+ "/",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',                 
        }

        with open(path + video_list[i]['title'] + '.mp4', 'wb') as f:
            print("-------------------------STart LINE-------------------------")
            print("第"+ str(i)+ "个视频:" + video_list[i]['title'] + " 开始下载")
            f.write(requests.get(video_url[i], headers = headers,verify = False).content)
            print( "下载完成")
            print("-------------------------STop LINE-------------------------")
    print("Done~")



def main():
    User_Mid = 176756724    # 这里放的就是你想下载的Up主的 mid 号
    Video_List = get_Mainpage_Video(User_Mid)
    Video_Url = get_video_url(Video_List)
    download(Video_Url, Video_List)

if __name__ == '__main__':
    main()

