from django.shortcuts import render,redirect
from crawler.crawler import fetch,parse_article_entries,parse_article_meta,get_meta_from_pages,get_metadata_from
#from crawler.models import PTTPost
from crawler import models
import time,math
from django.http import HttpResponse

# Create your views here.
def getPTT(request): #從第一頁開始抓
    start_url = 'https://www.ptt.cc/bbs/movie/index.html'
    metadata, link = get_meta_from_pages(start_url, num_pages=5)
    storemeta(metadata)
    linkunit = models.PTTLink.objects.create(link=link)
    linkunit.save()
    ans = 'success'
    return HttpResponse(ans)
def getPastPTT(request): #往回抓過去還未抓完的資料
    start = models.PTTLink.objects.latest()
    start_url = start
    metadata, link = get_meta_from_pages(start_url, num_pages=2)
    storemeta(metadata)
    linkunit = models.PTTLink.objects.create(link=link)
    linkunit.save()
    ans ='success'
    return HttpResponse(ans)
def getNews(request):
    if request.method =="POST":
        storemeta()
def storemeta(metadata):
    for meta in metadata:
        title = meta['title']
        push = meta['push']
        date = meta['date']
        author = meta['author']
        content = meta['content']
        times = meta['times']
        link = meta['link']
        unit = models.PTTPost.objects.create(title=title, push=push, date=date, author=author, content=content,times=times,link=link)
        unit.save()

def asktime(request):
    ans=time.strftime('%Y-%m-%d %H:%M.%S',time.localtime(time.time()))
    return HttpResponse(ans)
def index(request,pageindex=None):
    global page  # 重複開啟本網頁時需保留 page1 的值
    pagesize = 25  # 每頁顯示的資料筆數
    Posts = models.PTTPost.objects.all().order_by('-date')  # 讀取資料表,依時間遞減排序
    datasize = len(Posts)  # 資料筆數
    totpage = math.ceil(datasize / pagesize)  # 總頁數
    if pageindex == None:  # 無參數
        page = 0
        Posts = models.PTTPost.objects.order_by('-date')[:pagesize]
    elif pageindex == 'prev':  # 上一頁
        start = (page - 1) * pagesize  # 該頁第1筆資料
        if start >= 0:  # 有前頁資料就顯示
            Posts = models.PTTPost.objects.order_by('-date')[start:(start + pagesize)]
            page -= 1
    elif pageindex == 'next':  # 下一頁
        start = (page + 1) * pagesize  # 該頁第1筆資料
        if start < datasize:  # 有下頁資料就顯示
            Posts = models.PTTPost.objects.order_by('-date')[start:(start + pagesize)]
            page += 1
    currentpage = page + 1  # 將目頁前頁面以區域變數傳回html
    return render(request, "index.html", locals())
def content(request,detailid=None):
    Post = models.PTTPost.objects.get(id=detailid)
    return render(request, "content.html", locals())
