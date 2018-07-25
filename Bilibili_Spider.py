# coding: utf-8
# Writer: Mike_Shine
# Date: 2018-7-11
# 请尊重原创，谢谢。

# 这段代码是输入B站UP主的编号（User_Mid------进入up主的主页 https://space.bilibili.com/91236407/#/video。 其中91236407即为 User_Mid），然后爬取主页内的视频
# 有一点没有做的就是说这段代码只爬100个。如果想要爬所有的视频，你可以加一点点代码做翻页的动作，获取新的包

import json
import re
import os
import requests
import time

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
    if i>=100:
        i = 100
        video_List=[]
        for num in range(i):
            aid =  content['data']['vlist'][num]['aid']
            title = content['data']['vlist'][num]['title']
            author = content['data']['vlist'][num]['author']
            tmp = {"aid":aid,"title":title,"author":author}
            video_List.append(tmp)
        return video_List
    else:
        video_List=[]
        for num in range(i):
            aid =  content['data']['vlist'][num]['aid']
            title = content['data']['vlist'][num]['title']
            author = content['data']['vlist'][num]['author']
            tmp = {"aid":aid,"title":title,"author":author}
            video_List.append(tmp)
        return video_List

# 为了替换掉命名时的非法字符，不然下载创建路径时会报错
def sub(s):
    patn_1 = re.compile(r'\?')  
    patn_2 = re.compile(r'\/')
    patn_3 = re.compile(r'\\')
    patn_4 = re.compile(r'\|')
    patn_5 = re.compile(r'\:')
    patn_6 = re.compile(r'\<')
    patn_7 = re.compile(r'\>')
    patn_8 = re.compile(r'\*')
    patn_9 = re.compile(r'\:')

    s = re.sub(patn_1,"",s)
    s = re.sub(patn_2,"",s)
    s = re.sub(patn_3,"",s)
    s = re.sub(patn_4,"",s)
    s = re.sub(patn_5,"",s)
    s = re.sub(patn_6,"",s)
    s = re.sub(patn_7,"",s)
    s = re.sub(patn_8,"",s)
    s = re.sub(patn_9,"",s)
    return s 


# 下面是创建路径
def Get_Path(Video_List):
    path = r"D:/video/" + Video_List[0]['author']+ "/"
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


# 下载的函数
# 这里拿到URL就下载，因为URL是动态更新的，要注意这个点。
def download(i,Video_List,path):
    url = 'https://www.bilibili.com/video/av'+ str(Video_List[i]['aid'])      # 每个的Url
    html = requests.get(url, verify = False).text
    url_patn = re.compile(r'"url":"(.*?)","backup_url"')
    Video_Url = []
    Video_Url.append(re.findall(url_patn, html)[0])   # 这个是URL  
    
    #下面是下载内容
    headers = {
        'Host': 'data.bilibili.com', 
        'Connection': 'keep-alive',
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.bilibili.com/video/av'+ str(Video_List[i]['aid'])+ "/",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',                 
        }
    title = sub(str(Video_List[i]['title']))  # 防止有不合法的命名符号出现。
    with open(path + title + '.mp4', 'wb') as f:
        print("-------------------------STart LINE-------------------------")
        localtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print(localtime + "第"+ str(i+1)+ "个视频:" + Video_List[i]['title'] + " 开始下载")
        f.write(requests.get(Video_Url[0], headers = headers, verify = False).content)
        
        localtime = time.strftime("%Y-%m-%d %H:%M:%S")
        print( localtime + "下载完成")
        print("-------------------------STop LINE-------------------------")

# 主函数
def main():
    User_Mid = 91236407  # 在这里改你的Up主编号
    Video_List = get_Mainpage_Video(User_Mid)  # 拿到视频列表
    print(Video_List)  # 看一下你拿到的视频列表
    # 下面开始下载
    for i in range(len(Video_List)):
        download(i,Video_List,Get_Path(Video_List))


if __name__=='__main__':
    main()
    
