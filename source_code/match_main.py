#!/usr/bin/python
import glob
import re
import string
import md5
import pickle
import urllib2
import json
import time
import os
import base64
import urlparse
from multiprocessing import Process,Pool
#f=open('suspicious-document07100.txt','r')
#filenames=glob.glob("suspicious/suspicious-document11081.txt")

def matching(args):
    file_name=args[0]
    window_size=args[1]
    overlap_size=args[2]
    start=args[3]
    end=args[4]
    ip=args[5]
#    print file_name,window_size,overlap_size,start,end,ip
    os.system("sshpass -p \'ubuntu\' scp %s ubuntu@%s:~" %(file_name,ip))
    f=os.popen("sshpass -p \'ubuntu\' ssh ubuntu@%s \'python matching.py %s %s %s %s %s\'"  %(ip,file_name,window_size,overlap_size,start,end) )
    result=json.loads(f.read())
    return result

def reduce(results):
    result={}
    result.update( {'plain_text':[]} )
    for d in results:
        for key in d:
            if cmp(key,'plain_text')!=0:
                k=key[29:34]
                if result.has_key(k):
                    result[k]+=d[key]
                else:
                    result.update( {k:d[key]} )
            else:
                for m in d[key]:
                    if not (plain_text[m] in result[key]):
                        result[key]+=[ plain_text[m] ]

    return result




while True:
    try:
        url = "http://doraemon1293513.appspot.com/get_queue"
        s=urllib2.urlopen(url).read()

        s = base64.decodestring(s)
        data = json.loads(s)

    except (urllib2.HTTPError,ValueError):
        time.sleep(10)
    else:
	t0=time.time()
        ips=['131.227.75.75','131.227.75.70','131.227.75.77','131.227.75.66']
        window_size=data['window_size']
        overlap_size=data['overlap_size']
        file_key=data['key']
        number_of_instances=data['number_of_instances']
    #    number_of_instances=1


        url = "http://doraemon1293513.appspot.com/serve/"+file_key
        text = urllib2.urlopen(url).read().lower()
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        suspicious_index={}
	plain_text={}

    #build_suspicious_idex
        text=regex.sub('',text)
        text=text.decode('ascii','ignore').encode('ascii')
        text=" ".join(text.split()).split(' ')
        n=0
        while ( (window_size-overlap_size)*n+window_size < len(text)):
            start =(window_size-overlap_size)*n
            end= (window_size-overlap_size)*n+window_size
            n+=1
            temp_str=" ".join(word for word in text[start:end])
    #        print temp_str
            m=md5.new(temp_str).hexdigest()

            if suspicious_index.has_key(m):
                suspicious_index[m]+=1

            else:
                suspicious_index.update({m:1})
                plain_text[m]=temp_str

        if (window_size-overlap_size)*n+window_size>=len(text):
            temp_str=" ".join(word for word in text[(window_size-overlap_size)*n:])
    #        print temp_str
            m=md5.new(temp_str).hexdigest()
            n+=1
            if suspicious_index.has_key(m):
                suspicious_index[m]+=1
            else:
                suspicious_index.update({m:1})
                plain_text[m]=temp_str
    #

        file_name = str(time.time()).replace('.','')+ '.mindex'
        pickle.dump(suspicious_index,open(file_name,'wb'))
        print len(suspicious_index)
    #    start=30
    #    end=32
    #    parameters=[ [file_name,window_size,overlap_size,start,end,ips[3]] ]
        parameters=[]
        number=500/number_of_instances

        for i in range(number_of_instances):
            start=1+i*number
            if i==number_of_instances-1:
                end=500
            else:
                end=(i+1)*number

            parameters.append([file_name,window_size,overlap_size,start,end,ips[i]])


        pool = Pool(processes=number_of_instances)
        results=pool.map(matching,parameters)
        ans=reduce(results)
        ans.update( {'length':len(suspicious_index)} )
        ans.update( {'file_key':file_key} )
        pt=ans['plain_text']
        del ans['plain_text']
        s=''
        for key in ans.keys():
            s+=key+':'+str(ans[key])+';'
        s=s[:-1]
        url="http://doraemon1293513.appspot.com/result/"+s
        try:
            print urllib2.urlopen(url).read()
            
        except urllib2.HTTPError:
            print 'HTTPError(GAE)'
        else:       
            n=0
            print len(pt)
            while n<len(pt):
                s=';'.join(pt[n:n+10])
                u="http://doraemon1293513.appspot.com/plain_text/"+file_key+';'+s
                u=u.replace(' ','%20')
                print u
                n+=10
                try:
                    urllib2.urlopen(u).read()
                except urllib2.HTTPError:
                    print 'HTTPError(GAE)'
        os.system('rm -f %s' %file_name)
        print time.time()-t0
