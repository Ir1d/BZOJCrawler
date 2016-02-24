import urllib2
import Queue
import re
import os
import sys
import threading
q = Queue.Queue()
def html2pdf(idx):
    # cat="pdftk"
    html_path=workdir+'html/'+str(idx)+'.html'
    problem=workdir+'contest/'+str(idx)+'.pdf'
    cmd='./wkhtmltopdf --encoding utf-8'\
        ' %s %s'%(html_path,problem)
    print cmd
    os.popen(cmd)
    # cat+=' '+problem
    # lock.acquire()
    print "Generate:%d.pdf"%(idx)
    # lock.release()
    # print "OK!!!"
    # contest_path='"'+workdir+'contest/'+title+'.pdf"'
    # cat+=' cat output '+contest_path
    # os.popen(cat)
    # print "Merge:%s.pdf"%(title)
def mint(d):
    try:
        return int(d)
    except BaseException:
        return 0
def worker():
    global q
    while q.empty() != True:
        idx = q.get()
        html2pdf(idx)
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
if begin > end:
    begin, end = end, begin
l = dict(zip([i for i in xrange(begin, end + 1)], [False for x in xrange(begin, end + 1)]))
l[0] = True
f = open('qxt.txt', 'r')
lst = f.read().split('\n')
lst = map(mint, lst)
for i in lst:
    l[i] = True
for i in xrange(begin, end + 1):
    if (l[i] == False):
        q.put(i)
threads=int(sys.argv[3])
thds = list()
for i in xrange(threads):
    thds.append(threading.Thread(target=worker))
    thds[-1].start()
print 'using', threads, 'threads'

while q.empty() != True:
    pass
print 'work done!'
print 'exiting in 10secs'
time.sleep(10)
os.exit()