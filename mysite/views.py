from blog.youtube_crawling import main_crawling
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return main_crawling(request)
