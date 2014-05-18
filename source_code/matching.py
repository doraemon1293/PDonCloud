import sys
import pickle
import json
import urllib2
import os
import time
t0=time.time()
file_name=sys.argv[1]
window_size=int(sys.argv[2])
overlap_size=int(sys.argv[3])
start=int(sys.argv[4])
end=int(sys.argv[5])

#print file_name,window_size,overlap_size,start,end,number
suspicious_index = pickle.load(open(file_name,'rb'))
#print suspicious_index
url= "http://dualstack.build-index-1936582874.eu-west-1.elb.amazonaws.com/build_index?window_size=%s&overlap_size=%s&start=%s&end=%s" %(window_size,overlap_size,start,end)

source_index = json.load(urllib2.urlopen(url))
result={}
result['plain_text']=[]
for key in suspicious_index.keys():
    if source_index.has_key(key):
        if not key in result['plain_text']:
            result['plain_text']+=[key]
        for file in source_index[key]:
            if result.has_key(file):
                result[file]+=suspicious_index[key]
            else:
                result.update( {file:suspicious_index[key]} )
jsonarray=json.dumps(result,sort_keys=True)
os.system("rm -f %s" %file_name)
print jsonarray
