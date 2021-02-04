import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import io
import re

def main_crawling(request):
    # youtube 정보를 한국어로 가지고 오는 방법
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    url = "https://www.youtube.com/feed/trending"


    # Chrome 창을 열지않고 스크래핑하는 part
    options = webdriver.ChromeOptions()
    #options.headless = True       #webpage open 유형
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    browser = webdriver.Chrome(options=options) 
    browser.get(url)

    SCROLL_PAUSE_TIME = 0.5     # 한번 스크롤 하고 멈출 시간 설정
   

    body = browser.find_element_by_tag_name('body')
    #content = browser.find_element_by_id('content')

    # for i in range(3):

    #     time.sleep(SCROLL_PAUSE_TIME)
    #     height= browser.execute_script('return document.documentElement.scrollHeight')
       
    #     for j in range(5):
    #         body.send_keys(Keys.END)
    #         # body 본문에 END키를 입력(스크롤내림)
    #         time.sleep(SCROLL_PAUSE_TIME)

    soup = BeautifulSoup(browser.page_source, 'lxml')

    all_videos = soup.find_all(id='dismissable')

    video_img = []
    video_src = []
    video_title = []
    video_channel_name = []
    video_num = []
    video_writing = []

    
    for video in all_videos:

        Src = video.find('a',{'id':'thumbnail'})['href']+"https://www.youtube.com"
        video_src.append(Src)

        title = video.find('a',{'id':'video-title'})['title']
        video_title.append(title)

        channel_name = video.find('a',{"class":"yt-simple-endpoint style-scope yt-formatted-string"}).text
        video_channel_name.append(channel_name)

        num = video.find('span',{'class':"style-scope ytd-video-meta-block"}).text
        video_num.append(num)

        writing = video.find('yt-formatted-string',{'id':'description-text'}).text
        video_writing.append(writing)

        try:
            img = video.find('img',{'class':'style-scope yt-img-shadow'})
            video_img.append(img['src'])
        except:
            continue


        

    trending_videos = {"video_img":video_img, "video_src":video_src, "video_title":video_title, "video_channel_name":video_channel_name,"video_num":video_num, "video_writing":video_writing}

    browser.quit()

    return render(request, 'blog/home.html',trending_videos)










def crawling(get_url,request):

    # youtube 정보를 한국어로 가지고 오는 방법
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


    # Chrome 창을 열지않고 스크래핑하는 part
    options = webdriver.ChromeOptions()
    #options.headless = True       #webpage open 유형
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
    browser = webdriver.Chrome(options=options) 
    
    
    #입력한 url을 처리해주는 부분
    #만약에 youtube 채널 홈화면의 url을 가지고 오는 경우에 따로 처리를 해주는 과정
    if "videos" in get_url:
        url = get_url
    else:
        url = get_url+"/videos"

    browser.get(url)

    SCROLL_PAUSE_TIME = 0.5     # 한번 스크롤 하고 멈출 시간 설정
   

    body = browser.find_element_by_tag_name('body')
    # body태그를 선택하여 body에 넣음

    while True:
        last_height = browser.execute_script('return document.documentElement.scrollHeight')
        # 현재 화면의 길이를 리턴 받아 last_height에 넣음
        for i in range(10):
            body.send_keys(Keys.END)
            # body 본문에 END키를 입력(스크롤내림)
            time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            break;

    soup = BeautifulSoup(browser.page_source, 'lxml')

    # 채널명, 구독자수, 채널이미지 스크래핑
    channel_name = soup.find(id = 'text-container').text
    subscriber_count = soup.find(id = "subscriber-count").text
    channel_img = soup.find(id = "img")['src']

    


    # 채널의 영상 제목, 재생시간, 조회수, 업로드 시간 스크래핑
    all_videos = soup.find_all(id='dismissable')
    video_img = []
    title_list = [] #제목
    video_time_list = [] #재생시간
    view_num_list = [] #조회수
    video_upload_time_list = [] #업로드 시간
    view_num_regexp = re.compile(r'조회수')

    for video in all_videos:
        img = video.find('img',{'src':True})
        video_img.append(img['src'])


        title = video.find(id='video-title')
        title_list.append(title.text)

        video_time = video.find('span',{'class' : 'style-scope ytd-thumbnail-overlay-time-status-renderer'})
        video_time_list.append(video_time.text.strip())

        view_num = video.find('span',{'class':'style-scope ytd-grid-video-renderer'})
        if view_num_regexp.search(view_num.text):
            view_num_list.append(view_num.text)

        video_upload_time = video.find_all('span',{'class':'style-scope ytd-grid-video-renderer'})
        temp = video_upload_time[1].text
        video_upload_time_list.append(temp)

   
    channel_info = {"channel_url":url,"channel_name":channel_name,"subscriber_count":subscriber_count,"channel_img":channel_img,"video_img":video_img}
    browser.quit()
    #return render(request, 'blog/post_list.html', {"channel_name":channel_name,"subscriber_count":subscriber_count,"channel_img":channel_img})
    return render(request, 'blog/post_list.html', channel_info)
