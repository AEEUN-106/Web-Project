from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import io
import re


channel_info = {}
videos_info = []


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

    SCROLL_PAUSE_TIME = 0.15     # 한번 스크롤 하고 멈출 시간 설정

    body = browser.find_element_by_tag_name('body')
   
   # 스크롤 내리기
    for i in range(15):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)
    
    soup = BeautifulSoup(browser.page_source, 'lxml')
    all_videos = soup.find_all(id='dismissable')
    del all_videos[0]       # 첫번째 영상 중복을 없애기 위해서

    videos = [] # 전체 영상들을 저장하는 list

    for video in all_videos:
        one_video = []     # 영상 하나의 정보를 저장하는 list

        Src = "https://www.youtube.com"+video.find('a',{'id':'thumbnail'})['href']
        one_video.append(Src)    

        title = video.find('a',{'id':'video-title'})['title']
        one_video.append(title)
    
        channel_name = video.find('a',{"class":"yt-simple-endpoint style-scope yt-formatted-string"}).text
        one_video.append(channel_name)
     
        num = video.find('span',{"class":"style-scope ytd-video-meta-block"}).text
        one_video.append(num)
     
        writing = video.find('yt-formatted-string',{'id':'description-text'}).text
        one_video.append(writing)
     
        try:
            img = video.find('img',{'class':'style-scope yt-img-shadow'})
            one_video.append(img['src'])
        except:
            continue

        videos.append(one_video)
    
    
    browser.quit()
    trending_vidoes = {"videos" : videos}

    return render(request, 'blog/home.html',trending_vidoes)


def show_channel_info(url, request):

    global channel_info
    channel_info = crawling(url,request)

    return render(request, 'blog/post_list.html', channel_info)

def sort(sorting_method,request):
    #return render(request,'blog/post_list.html',{"channel_info":channel_info,"method":sorting_method})
    video_info = videos_info
    if sorting_method == "오래된순":
        if "년" not in video_info[0][3]:
            if "개월" not in video_info[0][3]:
                video_info.reverse()
                channel_info['videos'] = video_info


    elif sorting_method == "최신순":
       if "일" not in video_info[0][3]:
            if "주" not in video_info[0][3]:
                video_info.reverse()
                channel_info['videos'] = video_info
    
    elif sorting_method == "조회순":
        for i in range(len(video_info)):
            for j in range(i, len(video_info)):
                a = video_info[i][3]
                b = video_info[j][3]
                thousand = a.find("천")
                ten_thousand = a.find("만")
                hun_million = a.find("억")

                # if thousand != 0:
                #     a = a[4:thousand]
                # elif ten_thousand != 0:
                #     a = a[4:ten_thousand-1]
                # elif hun_million != 0:
                #     a = a[4:hun_million]
                # else:
                #     a = a[4:a.find("회")]
                
                print("---------------                " + a)
                # if thousand != 0:
                #     a = a[4:thousand-1]
                #     print(a)
                #     int_a = int(a) * 1000
                # elif ten_thousand != 0:
                #     a = a[4:ten_thousand-1]
                #     int_a = int(a) * 10000
                # elif hun_million != 0:
                #     a = a[4:hun_million-1]
                #     int_a = int(a) * 100000000
                # else:
                #     a = a[4:a.find("회")-1]
                #     int_a = int(a)

                thousand = b.find("천")
                ten_thousand = b.find("만")
                hun_million = b.find("억")

                # if thousand != 0:
                #     b = b[4:thousand-1]
                #     int_b = int(b) * 1000
                # elif ten_thousand != 0:
                #     b = b[4:ten_thousand-1]
                #     int_b = int(b) * 10000
                # elif hun_million != 0:
                #     b = b[4:hun_million-1]
                #     int_b = int(b) * 100000000
                # else:
                #     b = b[4:b.find("회")-1]
                #     int_b = int(b)

                # if int_a > int_b:
                #     temp = video_info[i]
                #     video_info[i] = video_info[j]
                #     video_info[j] = temp

                
                


                

            


    return render(request,'blog/post_list.html',channel_info)


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

    SCROLL_PAUSE_TIME = 0.15     # 한번 스크롤 하고 멈출 시간 설정

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

    try:
        channel_img = soup.find(id = "img")['src']
    except:
        print("예외")


    
    # 채널의 영상 제목, 재생시간, 조회수, 업로드 시간 스크래핑
    all_videos = soup.find_all(id='dismissable')
    view_num_regexp = re.compile(r'조회수')

    videos = []
    for video in all_videos:

        one_video= []

        Src = "https://www.youtube.com"+video.find('a',{'id':'thumbnail'})['href']
        one_video.append(Src)

        try:
            img = video.find('img',{'src':True})
            one_video.append(img['src'])
        except:
            continue

        title = video.find(id='video-title')
        one_video.append(title.text)

        # video_time = video.find('span',{'class' : 'style-scope ytd-thumbnail-overlay-time-status-renderer'})
        # one_video.append(video_time.text.strip())

        view_num = video.find('span',{'class':'style-scope ytd-grid-video-renderer'})
        if view_num_regexp.search(view_num.text):
            one_video.append(view_num.text)

        video_upload_time = video.find_all('span',{'class':'style-scope ytd-grid-video-renderer'})
        temp = video_upload_time[1].text
        one_video.append(temp)

        

        videos.append(one_video)

    
  
    browser.quit()
    channel_info = {"videos" :videos,"channel_name":channel_name,"subscriber_count":subscriber_count,"channel_img":channel_img,"channel_url":url}

    global videos_info
    videos_info = videos

    return channel_info
    # return render(request, 'blog/post_list.html', channel_info)
