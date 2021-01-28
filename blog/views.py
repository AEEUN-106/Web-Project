from django.shortcuts import render
from blog.youtube_crawling import *

# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})

def data_process(request):
    url = request.GET.get("Channel_Src")
    return crawling(url,request)
    #return render(request, 'blog/data_process.html', {"url":url})
