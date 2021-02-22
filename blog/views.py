from django.shortcuts import render
from blog.youtube_crawling import *


# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})

def data_process(request):
    url = request.GET.get("Channel_Src")
    return show_channel_info(url,request)

def Sorting(request):
    # year = request.GET.get("year")
    #month = request.GET.get("location=this.value;")
    sorting_method= request.GET.get("sorting")
    return sort(sorting_method,request)
