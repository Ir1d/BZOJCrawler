import urllib
import urllib2
import re
import os
import sys
import threading

def get_html(url):
	t = 50
	while t > 0:
		try:
			return urllib2.urlopen(url).read();
		except:
			t -= 1
	print "open url failed:%s" % url
def down_src(idx):
	nsrc = 'src/' + str(idx)
	# http://codeforces.com/contest/1/problems
	# http://www.lydsy.com/JudgeOnline/problem.php?id=1503
	# url = "http://codeforces.com/contest/" + str(idx)
	url = "http://www.lydsy.com/JudgeOnline/problem.php?id=" + str(idx)
	# open(workdir+nsrc,"w").write(get_html(url))
	html_path=workdir+'html/'+str(idx)+'.html'
	page = get_html(url)
	if page != None and len(page) != 0:
		open(html_path,'w').write(header+page)
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
			print "Done progress %d / %d" % (begin,size)
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
h_list=open(workdir+"html_list.txt","wb")
print "crawl contest %d to %d\n%d threads used,save in %s"%(begin,end,threads,workdir)
for i in range(threads):
	crawl_contest().start()
print "Work Done!"