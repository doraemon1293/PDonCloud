import re
import string
import md5
import pickle
import time
import json
import time
from mod_python import util
def index(req):
#	t0=time.time()
#	f=open('window_overlap_size','rb')
#	temp=f.readline()
#	t0=time.time()
	form = util.FieldStorage(req,keep_blank_values=1)
	window_size=int(form.getfirst("window_size"))
	overlap_size=int(form.getfirst("overlap_size"))
	start=int(form.getfirst("start"))
	end=int(form.getfirst("end"))
        filenames=[]
        for i in range(start,end+1):
                s="/source_files/source-document"+"%.5d" %i+".txt"
                print s
                filenames.append(s)
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	
	source_index={}
	for filename in filenames:
		f=open(filename,'r')
		text=f.read().lower()
		text=regex.sub('',text)
		text=text.decode('ascii','ignore').encode('ascii')
		text=" ".join(text.split()).split(' ')
		n=0
		while ( (window_size-overlap_size)*n+window_size < len(text)):
			start =(window_size-overlap_size)*n
			end= (window_size-overlap_size)*n+window_size
			n+=1
			temp_str=" ".join(word for word in text[start:end])
			m=md5.new(temp_str).hexdigest()
			if source_index.has_key(m):
				source_index[m].append(filename)
			else:
				source_index.update({m:[filename]})

		if (window_size-overlap_size)*n+window_size>=len(text):
			temp_str=" ".join(word for word in text[(window_size-overlap_size)*n:])
			m=md5.new(temp_str).hexdigest()
			if source_index.has_key(m):
				source_index[m].append(filename)
			else:
				source_index.update({m:[filename]})
		f.close()
	jsonarray = json.dumps(source_index)
#	print t1-t0
#		print filename
#	trantab = string.maketrans(',', ' ')
#	t1=time.time()
	return jsonarray
#	csv=open('source_index.csv','w')
#	csv.write('hash,files\n')
#	for key in source_index.keys():
#		csv.write(key+','+str(source_index[key]).translate(trantab)+'\n')
#	csv.close()
#	pickle.dump(source_index,open('source_index','wb'))
#	t1=time.time()
#	print t1-t0i
