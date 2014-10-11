import argparse
import threading
import requests
import json #print readable dictionary

#global variables
parser = argparse.ArgumentParser()
num_t = 10;
d = False;
threads = [];
html_data = [];
url = ""

#print only if in debug mode
def dprint(data):
    if d:
        print data

#thread class. run() performs the download.
class download_partial (threading.Thread):
    def __init__ (self, tid, begin, end):
        threading.Thread.__init__(self)
        self.tid = tid
        self.begin = begin
        self.end = end
        dprint("thread " + str(self.tid) + " created.")
        dprint("range: " + str(self.begin) + " " + str(self.end))

    #download data, store in html_data[self.tid]
    def run(self):
        r = requests.get(
            url,headers={"Accept-Encoding":"Identity", \
            "Range":"bytes="+str(self.begin)+"-"+str(self.end)})
        html_data[self.tid] = r.text

#parse arguments
parser.add_argument("-d", "--debug", help="verbosely print debug information while running", action="store_true")
parser.add_argument("url", help="the url to download")
parser.add_argument("-n", "--num_threads", help="number of threads to use in accelerator", type=int)
args = parser.parse_args()
if args.debug:
    d = True;
    dprint("debug turned on")
if args.num_threads:
    dprint('num_threads is ' + str(args.num_threads))
    num_t = args.num_threads

dprint("url is \"" + args.url + "\"")
url = args.url

#Get head
response = requests.head(url, headers={"Accept-Encoding":"Identity"})
try:
    dprint("Got response "+str(response.headers))
    length = int(response.headers['content-length'])
    dprint("Parsed length " + str(response.headers['Content-Length']))
except KeyError: #Content-Length header not returned
    print "Can't accelerate: Content length unavailable."
    quit()

#calculate length per thread
d_len = length / num_t

#Spin up threads
for t in range(0, num_t):
    html_data.append("")
    b = d_len * t
    e = d_len * (t+1) - 1
    if(t == num_t-1):
        e += (length % num_t)

    thread = download_partial(t, b, e)
    thread.start()
    threads.append( thread )

#Join threads
for thread in threads:
    thread.join()

f = open(url.split('/')[-1], 'w')
html_str = ''.join(html_data)
f.write(html_str)
