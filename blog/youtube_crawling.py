import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import io
import re
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")

url = "https://www.youtube.com/channel/UCVut4hqvrjQC4qDE3oc5qig/videos" # 임시:나중엔 예지언니가 받아온 url주소로 바꿔야됨
browser = webdriver.Chrome(options=options)
browser.get(url)

SCROLL_PAUSE_TIME = 0.5
# 한번 스크롤 하고 멈출 시간 설정

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

all_videos = soup.find_all(id='dismissable')
title_list = [] #제목
video_time_list = [] #재생시간
view_num_list = [] #조회수
video_upload_time_list = [] #업로드 시간
view_num_regexp = re.compile(r'조회수')

for video in all_videos:
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


print(len(title_list))
print(title_list)
print(len(video_time_list))
print(video_time_list)
print(len(view_num_list))
print(view_num_list)
print(len(video_upload_time_list))
print(video_upload_time_list)


browser.quit()
