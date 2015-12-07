'''
download the station feed

'''
#__author__ = 'Xia'

import sys
import urllib2
import json
import datetime as dt
import pandas as pd
import os
import time


while True:


	# load the json file online
	url = ('http://wservice.viabicing.cat/v2/stations')
	request = urllib2.urlopen(url)
	info = json.loads(request.read())

	# convert json file to pandas dataframe
	midd = json.dumps(info['stations'])
	data = pd.read_json(midd)
	ud = info['updateTime']
	ts = dt.datetime.fromtimestamp(ud).strftime(
	                           '%y_%m_%d_%H_%M_%S')

	# select only the useful columns
	x = data[['id', 'bikes', 'latitude', 
                'longitude', 'slots', 'status', 'type']]
	s = pd.DataFrame({'updateTime':[ud]* x.shape[0],
				  'id': data['id']})
	staInfo = pd.merge(x, s, on = 'id')

	# save the pd dataframe as csv
	# name of the file is the time of update
	staInfo.to_csv((os.getenv('ADS')+
	           'network_project/data/%s.csv' %ts), 
			    sep = ',', na_rep= 'NA')
	time.sleep(5*60)