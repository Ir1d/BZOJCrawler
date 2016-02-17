import urllib2
import re
import os
import sys
import threading


def html2pdf(idx):
	# cat="pdftk"
	html_path=workdir+'html/'+str(idx)+'.html'
	problem=workdir+'contest/'+str(idx)+'.pdf'
	cmd='wkhtmltopdf '\
		' %s %s'%(html_path,problem)
	print cmd
	os.popen(cmd)
	# cat+=' '+problem
	lock.acquire()
	print "Generate:%d.pdf"%(idx)
	lock.release()
	# print "OK!!!"
	# contest_path='"'+workdir+'contest/'+title+'.pdf"'
	# cat+=' cat output '+contest_path
	# os.popen(cat)
	# print "Merge:%s.pdf"%(title)

class gogogo(threading.Thread):
    def __init__(this):
        threading.Thread.__init__(this)
    def run(this):
    	global begin
    	while begin <= end:
	    	lock.acquire()
	    	# curcontest=contest[cur]
	    	curid = begin
	    	begin += 1
	    	html2pdf(curid)
	    	lock.release()
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
lock = threading.RLock()
print "%d threads used,save in %s"%(threads,workdir)
for i in range(threads):
	gogogo().start()
print "Work Done!"