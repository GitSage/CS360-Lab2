import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="verbosely print debug information while crunning", action="store_true")
parser.add_argument("url", help="the url to download")
parser.add_argument("-n", "--num_threads", help="number of threads to use in accelerator", type="int")
args = parser.parse_args()
if args.debug:
    print "debug turned on"
if args.url
    print "url is " + args.url
if args.num_threads
    print "num_threads is " + args.num_threads
