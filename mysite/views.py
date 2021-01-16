from django.http import HttpResponse

def index(request):
    html = "<html><body>예쥬 페이지</body></html>"
    return HttpResponse(html)
