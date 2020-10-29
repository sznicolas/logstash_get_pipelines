#!/usr/bin/python3

# get and format logstash pipeline stats


import argparse
import urllib.request, json 
from operator import itemgetter

# --- conf ---
lshost = 'localhost'
lsport = 9600
#url = "http://{}:{}/_node/stats/pipeline".format(lshost, lsport)
url = "http://{}:{}/_node/stats/pipelines".format(lshost, lsport)

# --- put colors in term ---
class pc:
    HEADER = '\033[95m'
    DATE   = '\033[31m'
    CYAN   = '\033[96m'
    BLUE   = '\033[94m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    ENDC   = '\033[0m'
    BOLD   = '\033[1m'
    UNDERLINE = '\033[4m'

# --- init options ---
parser = argparse.ArgumentParser(description='Prints logstash filter time execution')
parser.add_argument('-m',  help="minimum duration_in_millis", default=1, dest='md', type=int)
parser.add_argument('-c',  help="minimum count (input + output)", default=0, dest='count', type=int)
parser.add_argument('-t',  help="sort by total time (default: average per event)", action="store_true")
parser.add_argument('-f',  help="ignore events with no failure, except drop", action="store_true")
parser.add_argument('-v',  help="verbose", action="store_true")
parser.add_argument('url',  help="url to _node/stats/pipeline", default=url, nargs='?')

args = parser.parse_args()

# --- get data ---
print(args.url)
with urllib.request.urlopen(args.url) as api:
    data = json.loads(api.read().decode()) #, object_pairs_hook=OrderedDict)

data = data['pipelines']['main']['plugins']['filters']

# -- make stats ---
sl = {}
i = 0
for item in data:
    if (item['events']['in'] + item['events']['out'] <= args.count ):
        if args.v:
            print("Skip '{}' ; not enough input/output".format(item))
    elif (item['events']['duration_in_millis'] < args.md):
        if args.v:
            print("Skip '{}' ; no duration".format(item))
    elif (args.f and item.get("failures", 0) < 1 and item['name'] != 'drop'):
        if args.v:
            print("Skip '{}' ; no failure".format(item))
    else:
        data[i]['avg_time'] = round (item['events']['duration_in_millis'] / item['events']['in'], 4)
        if args.t :
            sl[i] = data[i]['events']['duration_in_millis']
        else:
            sl[i] = data[i]['avg_time']
    i += 1

# --- display results ---

# header
print(pc.HEADER + pc.BOLD + "{:25} {:10} {:>10} {:>10} {:>10} {:>6} {:8}".format("id", "name", "out", "in", "durat°(ms)", "avg(ms)", "failures"))
print("{:-<25} {:-<10} {:->10} {:->10} {:->10} {:->6} {:->8}".format("-", "-", "-", "-", "-", "-", "-") + pc.ENDC)

# loop
for k,v in sorted(sl.items(), key=itemgetter(1), reverse=True):
    if data[k]['name'] == "drop":
        print(pc.YELLOW, end="")
    elif data[k]['name'] == "useragent":
        print(pc.GREEN, end="")
    elif data[k]['name'] == "grok":
        print(pc.BLUE, end="")
    elif data[k]['name'] == "date":
        print(pc.DATE, end="")
    elif data[k]['name'] == "mutate":
        print(pc.CYAN, end="")
 
    print("{:25} {:10} {:>10} {:>10} {:>10} {:>6.4f} {:>8}".format(
        data[k]['id'][:25], data[k]['name'], data[k]['events']['out'], data[k]['events']['in'],
            data[k]['events']['duration_in_millis'], data[k]['avg_time'], data[k].get('failures', "-") )
         + pc.ENDC)
