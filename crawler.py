import urllib
import urllib2
import re
import os
import sys
import threading
import cookielib
from urllib import urlencode
from bs4 import BeautifulSoup
# from config import usr, pwd
usr = os.environ['BZOJUSERNAME']
pwd = os.environ['BZOJUSERPASS']
reload(sys)
sys.setdefaultencoding('utf-8')
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)
def login(usnm, pswd):
    h1={'Connection':'keep-alive', 'Accept-Language':'zh-CN,zh;q=0.9', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Cache-Control':'max-age=0', 'Upgrade-Insecure-Requests':'1', 'Host':'www.lydsy.com', 'DNT':'1', 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Accept-Encoding':'gzip, deflate, br'}
    # global cookie
    # print str(cookie)
    headers = {
        'Host': 'www.lydsy.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Origin': 'https://www.lydsy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 OPR/35.0.2066.37',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.lydsy.com/JudgeOnline/loginpage.php'
        }
    form = {
        'user_id':usnm,
        'password':pswd,
        'submit':'Submit'
    }
    
    postdata = urlencode(form)
    req = urllib2.Request('https://www.lydsy.com/JudgeOnline/login.php', postdata, headers)
    resp = urllib2.urlopen(req)
    # r = urllib2.urlopen('http://www.lydsy.com/Judgenline/modifypage.php')
    # print r.read()
    # ............................................................
login(usr, pwd)
    # ...........................................................
# import sys
# sys.exit()
def get_html(url):
    headers = {
        'Host': 'www.lydsy.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Origin': 'https://www.lydsy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 OPR/35.0.2066.37',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.lydsy.com/JudgeOnline/loginpage.php'
        }

    t = 50
    while t > 0:
        try:
            req = urllib2.Request(url, headers)
            return urllib2.urlopen(req).read();
        except:
            t -= 1
    print "open url failed:%s" % url
def saveImg(imageURL,fileName):
    headers = {
        'Host': 'www.lydsy.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Origin': 'https://www.lydsy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 OPR/35.0.2066.37',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.lydsy.com/JudgeOnline/loginpage.php'
        }
    print "start to fetch image on url:%s, name:%s" % (imageURL, fileName)
    req = urllib2.Request(imageURL, headers)
    u = urllib2.urlopen(req)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    f.close()
def get_image(idx, html):
    # print html
    # <img src="image/logo.png"/>
    pattern = re.compile('')
    soup = BeautifulSoup(html, "lxml")
    # print soup
    for img in soup.find_all('img'):
        src = img.get('src')
        if src[0] == '/':
            link = "https://www.lydsy.com"
        else:
            link = "https://www.lydsy.com/JudgeOnline/" + src
        saveImg(link, "html/" + src)
qxt = open('qxt.txt', 'w')
h_list=open("html_list.txt","wb")
def down_src(idx):
    headers = {
        'Host': 'www.lydsy.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Origin': 'https://www.lydsy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 OPR/35.0.2066.37',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.lydsy.com/JudgeOnline/loginpage.php'
        }
    url = "https://www.lydsy.com/JudgeOnline/problem.php?id=" + str(idx)
    try:
        req = urllib2.Request(url, headers)
        s = urllib2.urlopen(req).read()
    except BaseException:
        s = None
        print "Got exception on url %s!" % url
    if s:
        if (s.find('Please contact lydsy2012@163.com!') != -1):
            qxt.write('%d\n'%idx)
        s = s.replace('user='+usr, 'user=free_bzoj').replace('>%s<'%usr, '>free_bzoj<')
        page = BeautifulSoup(s, "lxml")
        
        lst = page.find_all('img')
        for i in lst:
            try:
                if i['src'][0] == '/':
                    picurl = 'https://www.lydsy.com' + i['src']
                elif i['src'][0:5] == 'https:':
                    pass
                else:
                    picurl = 'https://www.lydsy.com/JudgeOnline/' + i['src']
                if i['src'] != 'image/logo.png':
                    req = urllib2.Request(picurl, headers)
                    temppic = urllib2.urlopen(req).read()
                    f = open('html/image/%s'%str(i['src']).replace('.', '_').replace('/', '_'), 'wb')
                    f.write(temppic)
                    f.close()
                i['src'] = 'image/' + str(i['src']).replace('.', '_').replace('/', '_')
            except BaseException:
                print 'Got Exception while parsing img, src=' + i['src']
        page = str(page)
        f = open('html/%d.html'%idx, 'w')
        h_list.write('html/%d.html'%idx)
        f.write(header + page)
        f.close()
    # nsrc = 'src/' + str(idx)
    # # https://www.lydsy.com/JudgeOnline/problem.php?id=1503
    # # open(workdir+nsrc,"w").write(get_html(url))
    # html_path=workdir+'html/'+str(idx)+'.html'
    # lst = page.find_all('img')
    # lst
    # # os.system("mkdir html/images/%d" % idx)
    # get_image(idx, page)
    # if page != None and len(page) != 0:
    #     open(html_path,'w').write(header+page)
class crawl_contest(threading.Thread):
    def __init__(this):
        threading.Thread.__init__(this)
    def run(this):
        global begin
        while begin <= end:
            lock.acquire()
            curid = begin
            begin += 1
            lock.release()
            down_src(curid)
            print "Done progress %d / %d" % (begin,end)
arglen=len(sys.argv)
if arglen<4 or arglen>5:
    print "Usage:\n\t%s begin end threads [workdir]"%sys.argv[0]
    exit()
if arglen==5:
    workdir=sys.argv[4]
else:
    workdir="./"
begin=int(sys.argv[1])
end=int(sys.argv[2])
threads=int(sys.argv[3])
size = end - begin + 1
for d in ['src','html']:
    d=workdir+d
    if not os.path.exists(d):
        print "makedirs:%s"%d
        os.makedirs(d)
lock = threading.RLock()
header=open("header.html").read()
print "crawl contest %d to %d\n%d threads used,save in %s"%(begin,end,threads,workdir)
for i in range(threads):
    crawl_contest().start()
print "Work Done!"
