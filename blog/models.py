from django.conf import settings
from django.db import models
from django.utils import timezone
from youtube_crawling import title_list, video_time_list, view_num_list, video_upload_time_list

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    video_title = title_list #제목
    video_time = video_time_list #재생시간
    video_view_num = view_num_list #조회수
    video_upload_time = video_upload_time_list #업로드 시간
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
