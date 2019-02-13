import requests
from requests_html import HTML
import urllib.parse

def fetch(url): #抓下html內容
    response = requests.get(url, cookies={'over18': '1'})
    return response
def parse_article_entries(doc,classstring): #分析html框架 抓取class中的內容
    html = HTML(html=doc)
    post_entries = html.find(classstring)
    return post_entries
def parse_article_meta(entry): #將 r-ent 中的文章title資訊進行處理
    meta = {
        'title': entry.find('div.title', first=True).text,
        'push': entry.find('div.nrec', first=True).text,
        'date': entry.find('div.date', first=True).text,
    }
    try:
       meta['author']= entry.find('div.author', first=True).text
       contentlink= entry.find('div.title > a', first=True).attrs['href'] #存文章link
       # 抓各個文章的內文 存在responsecontent
       #if (contentlink!=None):
       meta['link'] = urllib.parse.urljoin('https://www.ptt.cc', contentlink)
       print (contentlink)
       responsecontent = fetch(meta['link'])
       content = parse_article_entries(responsecontent.text,'#main-container')
       #判斷 content 抓到的內容長度 文章存在的情況會有4個 article-meta-value
       if (len(content)>0  and len(content[0].find('span.article-meta-value'))==4):
           meta['times'] = content[0].find('span.article-meta-value')[3].text
           meta['content'] = content[0].text.split('※ 發信站')[0].split(meta['times'])[1]
       else:
           meta['content'] = '404 not found.'
           meta['times'] = ''
    except AttributeError:
        if '(本文已被刪除)' in meta['title']:
            match_author = meta['title'].split('[')
            if match_author:
                meta['author'] = match_author[1].replace(']','')
            meta['content'] = '404 not found.'
            meta['times'] = ''
            meta['link'] = ''
        elif '-' in meta['author']:#文章轉移至別版時 作者欄會出現'-'
            meta['content'] = '404 not found.'
            meta['times'] = ''
            meta['link'] = ''
    return meta
def get_metadata_from(url):
    def parse_next_link(doc): #儲存放在a.btn.wide第二個的上一頁連結
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return urllib.parse.urljoin('https://www.ptt.cc', link)

    resp = fetch(url) #抓html整頁內容
    post_entries = parse_article_entries(resp.text,'div.r-ent')#抓class中內容
    next_link = parse_next_link(resp.text) #儲存上一頁的link
    print ('next:',next_link)
    metadata = [parse_article_meta(entry) for entry in post_entries] #將class中內容分類放好
    return metadata, next_link
def get_meta_from_pages(url, num_pages): # 主要function 抓取從start_url 開始 到num_pages 數量的PTT文章
    collected_meta = [] #儲存所有的meta 資料
    for _ in range(num_pages):
        posts, link = get_metadata_from(url) #儲存該頁的貼文內容 以及 下一次要抓的link
        collected_meta += posts #將該頁內容儲存在collected中 全部抓取完畢後回傳
        url = urllib.parse.urljoin('https://www.ptt.cc', link)

    return collected_meta,url
