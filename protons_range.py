import numpy as np
from urllib2 import urlopen
from StringIO import StringIO
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties
from dateutil.relativedelta import relativedelta

def plot_summed_proton_lcurves(t1, t2, stereo, sept_tres, let_tres, het_tres):
	
	"""Read in STEREO proton data from the SEPT, LET and HET instruments and 
	make a plot. """

	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")

	tt = dt1

	#set up figure
	nl = 10
	xc = 255/nl
	f, ax = plt.subplots(figsize=(8,4))


	tt0 = datetime.datetime.strftime(tt, "%d-%b-%Y %H:%M")
		
	sept = 0
	# try:
	# 	#LET 1.8 - 10 MeV protons
	# 	sept_dates0, sept_lcurve = sept_proton_lcurve_range(t1, t2, stereo, '1')

	# 	s1 = ax.plot(sept_dates0, sept_lcurve[:,0], c = cm.rainbow(0 * xc + 1) ,label='SEPT 0.08 - 0.16 MeV')
	# 	s2 = ax.plot(sept_dates0, sept_lcurve[:,1], c = cm.rainbow(1 * xc + 1) ,label='SEPT 0.16 - 0.31 MeV')
	# 	s3 = ax.plot(sept_dates0, sept_lcurve[:,2], c = cm.rainbow(2 * xc + 1) ,label='SEPT 0.31 - 0.62 MeV')
	# 	s4 = ax.plot(sept_dates0, sept_lcurve[:,3], c = cm.rainbow(3 * xc + 1) ,label='SEPT 0.62 - 1.25 MeV')

	# 	#if there's sept data then use sept_dates0 to set xaxis times
	# 	ax.set_xlabel("Start Time "+dt1.strftime("%d-%b-%Y %H:%M")+" (UTC)")
	# 	sept = 1

	# except: 
	# 	print "No SEPT data for " + tt0

	let = 0
	try:
		#LET 1.8 - 10 MeV protons
		let_dates0, let_lcurve = parse_let_proton_range(t1, t2, stereo, '10')
		mxlet = np.max(let_lcurve)

		#l1 = ax.plot(let_dates0, let_lcurve[:,0], c = cm.rainbow(4 * xc + 1) ,label='LET 1.8 - 3.6 MeV')
		#l2 = ax.plot(let_dates0, let_lcurve[:,1], c = cm.rainbow(5 * xc + 1) ,label='LET 4 - 6 MeV')
		#l3 = ax.plot(let_dates0, let_lcurve[:,2], c = cm.rainbow(6 * xc + 1) ,label='LET 6 - 10 MeV')
		#l4 = ax.plot(let_dates0, let_lcurve[:,3], c = cm.rainbow(3 * xc + 1) ,label='LET 10 - 15 MeV')

		l1 = ax.plot(let_dates0, let_lcurve[:,0], c = cm.rainbow(1 * xc + 1) ,label='LET 1.8 - 3.6 MeV')
		l2 = ax.plot(let_dates0, let_lcurve[:,1], c = cm.rainbow(3 * xc + 1) ,label='LET 4 - 6 MeV')
		l3 = ax.plot(let_dates0, let_lcurve[:,2], c = cm.rainbow(5 * xc + 1) ,label='LET 6 - 10 MeV')
		

		#if there isn't any sept data, use het_dates0 to set xaxis times
		if sept == 0:
			ax.set_xlabel("Start Time "+dt1.strftime("%d-%b-%Y %H:%M")+" (UTC)")
		let = 1

	except:
		print "No LET data for " + tt0

	het = 0
	try:
		
		#HET 14 - 100 MeV protons
		het_dates0, het_lcurve = het_proton_lcurve_range(t1, t2, stereo, '15')
		mxhet = np.max(het_lcurve)

		#h1 = ax.plot(het_dates0, het_lcurve[:,0], c = cm.rainbow(7 * xc + 1) ,label='HET 15 - 24 MeV')
		#h2 = ax.plot(het_dates0, het_lcurve[:,1], c = cm.rainbow(8 * xc + 1) ,label='HET 24 - 40 MeV')
		#h3 = ax.plot(het_dates0, het_lcurve[:,2], c = cm.rainbow(9 * xc + 1) ,label='HET 40 - 60 MeV')

		h1 = ax.plot(het_dates0, het_lcurve[:,0], c = cm.rainbow(6 * xc + 1) ,label='HET 15 - 24 MeV')
		h2 = ax.plot(het_dates0, het_lcurve[:,1], c = cm.rainbow(8 * xc + 1) ,label='HET 24 - 40 MeV')
		h3 = ax.plot(het_dates0, het_lcurve[:,2], c = cm.rainbow(10 * xc + 1) ,label='HET 40 - 60 MeV')

		#if there isn't any sept data, use het_dates0 to set xaxis times
		if np.logical_and(sept == 0, let == 0):
			ax.set_xlabel("Start Time "+dt1.strftime("%d-%b-%Y %H:%M")+" (UTC)")
		het =1

	except:
		print "No HET data for " + tt0


	#format of tick labels
	hrsFmt = mdates.DateFormatter('%d')
	ax.xaxis.set_major_formatter(hrsFmt)
	ax.set_xlabel("Start Time "+t1+" (UTC)")
	ax.set_xlim([dt1, dt2])
	ymax = np.max([mxlet, mxhet])
	ax.set_ylim(top = ymax)
	ax.set_ylim(bottom = 1.e-4)

	#auto orientate the labels so they don't overlap
	#f.autofmt_xdate()

	#set yaxis log
	ax.set_yscale('log')

	#Axes labels
	ax.set_title("ST"+stereo.capitalize()+" Protons")
	ax.set_ylabel('H Intensity $\mathrm{(cm^{2}\,sr\,s\,MeV)^{-1}}$')

	#legend
	fontP = FontProperties()
	fontP.set_size('x-small')

	leg = ax.legend(loc='best', prop = fontP, fancybox=True )
	leg.get_frame().set_alpha(0.5)

	#month
	year = tt.year
	month = tt.month

	plt.show()
	#plt.savefig('/Users/hazelbain/Dropbox/proposals/ISSI14/figs/ST'+stereo.capitalize()+'_proton.jpeg', format='jpeg')


	return None




def sept_proton_lcurve_range(t1, t2, stereo, tres):

	"""STEREO SEPT OMNIDIECTIONAL 0.08 - 1.25 MeV proton lcurve from t1 to t2. 
	stereo = spacecraft name 'a' or 'b'
	tres = temporal resolution ('1' or '10' minute resolution)
	"""


	#get the url for each data file on the server
	urlfile = fetch_sept_ascii_url_range(t1, t2, stereo, tres)

	#loop through all urls, open file, read and concatenate into numpy array
	for f in range(len(urlfile)):

		#open and read data files
		txt = urlopen(urlfile[f]).read()
		ss = StringIO(txt.split('BEGIN DATA\n')[1])
		data_tmp = np.loadtxt(ss)

		#concatenate files
		if f == 0:
			data = data_tmp
		else:
			data = np.concatenate([data, data_tmp], axis = 0)


	#Time axis
	year = int(data[0][1])
	doy = int(data[0][2])
	hour = int(data[0][3])
	mins = int(data[0][4])
	secs = int(data[0][5])
	
	#create array of dates and times	
	dates0 = []
	for x in range(0,len(data)):
		dates0.append(datetime.datetime(year, 1, 1, 0, 0) + datetime.timedelta(days = int(data[x, 2]) - 1, hours = int(data[x, 3]), minutes = int(data[x, 4]), seconds = int(data[x, 5])))
			
	#SEPT 0.084 - 6.5 MeV lightcurve
	
	#sept_lcurve0 = np.sum(data[:, 6:11], axis = 1)
	#sept_lcurve1 = np.sum(data[:, 11:17], axis = 1)
	#sept_lcurve2 = np.sum(data[:, 17:23], axis = 1)
	#sept_lcurve3 = np.sum(data[:, 23:29], axis = 1)
	#sept_lcurve4 = np.sum(data[:, 29:35], axis = 1)

	sept_lcurve0 = np.sum(data[:, 6:12], axis = 1)
	sept_lcurve1 = np.sum(data[:, 12:19], axis = 1)
	sept_lcurve2 = np.sum(data[:, 19:25], axis = 1)
	sept_lcurve3 = np.sum(data[:, 25:31], axis = 1)

		
	sept_lcurve = np.concatenate([[sept_lcurve0], [sept_lcurve1], [sept_lcurve2], [sept_lcurve3]], axis = 0).T
		

	return dates0, sept_lcurve


def parse_let_proton_range(t1, t2, stereo, tres):

	"""STEREO LET SUMMED 1.8 - 10 MeV proton lcurve from t1 to t2 (format e.g. '18-aug-2010 00:00')
	stereo = spacecraft name 'a' or 'b'
	tres = temporal resolution ('1' or '10' minute resolution)"""

	#Get the URL of the data files on the server
	urlfile = fetch_let_ascii_url_range(t1, t2, stereo, tres)

	#if stereo == 'a':
	#	website = 'http://www.srl.caltech.edu/STEREO/DATA/Level1/Public/ahead/10Minute/2011/Summed/H/'
	#	files = np.asarray(['H_summed_ahead_2011_09_10min_level1_11.txt','H_summed_ahead_2011_10_10min_level1_11.txt'])
	#else:
	#	website = 'http://www.srl.caltech.edu/STEREO/DATA/Level1/Public/behind/10Minute/2011/Summed/H/'
	#	files = np.asarray(['H_summed_behind_2011_09_10min_level1_11.txt','H_summed_behind_2011_10_10min_level1_11.txt'])

	#loops through the list of urls and opens and read files and concatenate data 
	for i in range(len(urlfile)):
		try:
			
			#open and read data files
			txt = urlopen(urlfile[i]).read()
			ss = StringIO(txt.split('BEGIN DATA\n')[1])
			data_tmp = np.loadtxt(ss)

			#concatenate data
			if i == 0:
				data = data_tmp
			else:
				data = np.concatenate([data, data_tmp], axis = 0)

		except:
			print "Something wrong with LET file " + website + files[i]


		#Time axis
		year = int(data[0][0])
		doy = int(data[0][1])
		hour = int(data[0][2])
		mins = int(data[0][3])
		secs = int(data[0][4])

		dates0 = []
		for x in range(0,len(data)):
			dates0.append(datetime.datetime(year, 1, 1, 0, 0) + datetime.timedelta(days = int(data[x, 1]) - 1, hours = int(data[x, 2]), minutes = int(data[x, 3]), seconds = int(data[x, 4])))

		#LET 1.8 - 10 MeV lightcurve
		if tres == '1':
			let_lcurve = data[:, 7:10]
		elif tres == '10':
			let_lcurve = data[:, 6:9]


	return dates0, let_lcurve


def het_proton_lcurve_range(t1, t2, stereo, tres):

	"""STEREO HET SUMMED 14 - 100 MeV proton lcurve from t1 to t2 (e.g. format '18-aug-2010 00:00')
	stereo = spacecraft name 'a' or 'b'
	tres = temporal resolution ('15' minute resolution)
	"""

	#Get the URL of the data files on the server
	urlfile = fetch_het_ascii_url_range(t1, t2, stereo, tres)

	#if stereo == 'a':
	#	website = 'http://www.srl.caltech.edu/STEREO/DATA/HET/Ahead/15minute/'
	#	files = ['AeH11Sep.15m','AeH11Oct.15m']
	#else: 
	#	website = 'http://www.srl.caltech.edu/STEREO/DATA/HET/Behind/15minute/'
	#	files = ['BeH11Sep.15m','BeH11Oct.15m']


	#loops through URLs. Open and read data files, and concatenate the data
	for i in range(len(urlfile)):

		try:
			#read the file
			txt = urlopen(urlfile[i]).read()
			ss_tmp = StringIO(txt.split('End\r\n')[1])

			#----the variable names are listed in the header of each data files, I was lazy and called them vX
			if tres == '1':
				data_tmp = np.loadtxt(ss_tmp, dtype = {'names': ('v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16', \
				'v17','v18','v19','v20','v21','v22','v23','v24','v25','v26','v27','v28','v29','v30','v31','v32','v33'), \
				'formats': ('f4', 'f4', 'S3', 'f4', 'S4', 'f4', 'S3', 'f4', 'S4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4',\
				'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')})

			#----NOTE file formats change between file of different temporal resolution
			elif tres == '15':
				data_tmp = np.loadtxt(ss_tmp, dtype = {'names': ('v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16', \
				'v17','v18','v19','v20','v21','v22','v23','v24','v25','v26','v27','v28','v29','v30','v31','v32','v33',\
				'v34','v35','v36','v37'), \
				'formats': ('f4', 'f4', 'S3', 'f4', 'S4', 'f4', 'S3', 'f4', 'S4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4',\
				'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4',\
				'f4', 'f4', 'f4', 'f4')})
			else:
				print "No such temporal resolution for HET"

			if i == 0:
				data = data_tmp
			else:
				data = np.concatenate([data, data_tmp], axis = 0)

		except:
			print "Something wrong with HET file " + urlfile[i]

				
		#set up lightcurve variables
		year = data['v2']
		month = data['v3']
		day = data['v4']
		hour = data['v5']
		mins = data['v5']
					
		#append date
		dates0 = []
		for i in range(len(year)):
			month_tmp = datetime.datetime.strptime(month[i], "%b").month
			hr_tmp = int(hour[i][0:2])
			mn_tmp = int(mins[i][2:4])
			dates0.append(datetime.datetime(year[i], month_tmp, day[i], hr_tmp, mn_tmp))
		dates0 = np.asarray(dates0)

		#sum HET 14 - 100 MeV proton energies and append
		if tres == '1':
			h1 = np.sum([data['v13'],data['v15'],data['v17']],axis=0)
			h2 = np.sum([data['v19'],data['v21'],data['v23'],data['v25']],axis=0)
			h3 = data['v27']
		elif tres == '15':
			h1 = np.sum([data['v18'],data['v20'],data['v22']],axis=0)
			h2 = np.sum([data['v24'],data['v26'],data['v28'],data['v30']],axis=0)
			h3 = data['v32']
		else:
			print "No such temporal resolution for HET"


		het_lcurve = np.transpose(np.asarray([h1,h2,h3]))

	return dates0, het_lcurve


def fetch_let_ascii_url_range(t1, t2, stereo, tres):

	"""Determine the URL of the SECTORED STEREO LET 4-6 MeV protons txt files for times between t1 and t2 
	with temporal resoultion res.

	t1 = start time in ut format i.e. '18-aug-2010 00:00'
	t2 = end time
	stereo = 'A' or 'B' for sta/stb
	res = temporal resoluion either 1 or 10 for 1 and 10 minute summed files
	"""

	#determine the correct dates to the data files for
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")	
	year1 = dt1.year 
	month1 = dt1.month
	doy1 = date2doy(t1)
	doy2 = date2doy(t2)

	#correction if nmonths spans 2 years
	nyears = dt2.year - dt1.year + 1
	if nyears == 1:
		nmonths = dt2.month - dt1.month + 1
	elif nyears == 2:
		nmonths = (12 - dt1.month +1) + dt2.month
	else:
		print "Code currently doesn't span more than 2 calander years"

	#number of days
	ndays = dt2 - dt1 
	ndays = ndays.days + 1

	# STEREO A or B
	if stereo == 'a':
		st = 'ahead'
	if stereo == 'b':
		st = 'behind'

	#which instrument
	if tres == '1':
		
		url = []

		if nyears == 1:
			doy = doy1
			while doy <= doy2:			#montly URLs

				year = year1

				website = 'http://www.srl.caltech.edu/STEREO/DATA/Level1/Public/'+st+'/'+tres+'Minute/'+str(year)+'/Summed/H/'
				f = 'H_summed_'+st+'_'+str(year)+'_'+str(doy).zfill(3)+'_level1_11.txt'

				doy = doy + 1

				url.append(website + f)

	elif tres == '10':

		url = []

		for i in range(nmonths):			#montly URLs

			year = year1

			#set the month
			month = month1 + i
			if month > 12:
				year = year + (month/12)
				month = month - 12

			website = 'http://www.srl.caltech.edu/STEREO/DATA/Level1/Public/'+st+'/'+tres+'Minute/'+str(year)+'/Summed/H/'
			f = 'H_summed_'+st+'_'+str(year)+'_'+str(month).zfill(2)+'_10min_level1_11.txt'
			

			url.append(website + f)


	else:
		print "No such temporal resolution for LET"


	return url


def fetch_het_ascii_url_range(t1, t2, stereo, tres):

	"""Determine the URL of the SECTORED STEREO HET protons txt files for times between t1 and t2 
	with temporal resoultion res.

	t1 = start time in ut format i.e. '18-aug-2010 00:00'
	t2 = end time
	stereo = 'A' or 'B' for sta/stb
	res = temporal resoluion either 1 or 10 for 1 and 10 minute summed files
	"""

	#determine the correct dates to the data files for
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")	
	year1 = dt1.year 
	month1 = dt1.month
	doy1 = date2doy(t1)
	doy2 = date2doy(t2)

	#correction if nmonths spans 2 years
	nyears = dt2.year - dt1.year + 1
	if nyears == 1:
		nmonths = dt2.month - dt1.month + 1
	elif nyears == 2:
		nmonths = (12 - dt1.month +1) + dt2.month
	else:
		print "Code currently doesn't span more than 2 calander years"

	#number of days
	ndays = dt2 - dt1 
	ndays = ndays.days + 1

	# STEREO A or B
	if stereo == 'a':
		st = 'ahead'
	if stereo == 'b':
		st = 'behind'

	url = []

	month = month1
	for i in range(nmonths):			#montly URLs
		year = year1

		#set the month
		if month > 12:
			year = year + (month/12)
			month = month - 12

		month2 = datetime.datetime(2010, month, 1).strftime('%b')

		website = 'http://www.srl.caltech.edu/STEREO/DATA/HET/'+st.title()+'/'+tres+'minute/'
		f = st[0].title()+'eH'+str(year)[2:4]+month2+'.'+tres+'m'

		#print website+f

		url.append(website + f)

		month = month + 1


	return url


def fetch_sept_ascii_url_range(t1, t2, stereo, tres):

	"""Determine the URL of the SECTORED STEREO SEPT protons txt files for times between t1 and t2 
	with temporal resoultion res.

	t1 = start time in ut format i.e. '18-aug-2010 00:00'
	t2 = end time
	stereo = 'A' or 'B' for sta/stb
	res = temporal resoluion either 1 or 10 for 1 and 10 minute summed files
	"""

	#determine the correct dates to the data files for
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")	
	year1 = dt1.year 
	month1 = dt1.month
	doy1 = date2doy(t1)
	doy2 = date2doy(t2)

	#correction if nmonths spans 2 years
	nyears = dt2.year - dt1.year + 1
	if nyears == 1:
		nmonths = dt2.month - dt1.month + 1
	elif nyears == 2:
		nmonths = (12 - dt1.month +1) + dt2.month
	else:
		print "Code currently doesn't span more than 2 calander years"

	#number of days
	ndays = dt2 - dt1 
	ndays = ndays.days + 1

	# STEREO A or B
	if stereo == 'a':
		st = 'ahead'
	if stereo == 'b':
		st = 'behind'


	url = []

	if nyears == 1:

		#for i in range(doy.size):
		year = year1
		doy = doy1
		while doy <= doy2:

			#doytmp = str(doy.astype('S3'))
			website = 'http://www2.physik.uni-kiel.de/stereo/data/sept/level2/'+st+'/'+tres+'min/'+str(year)+'/'
			f = 'sept_'+st+'_ion_omni_'+str(year)+'_'+str(doy).zfill(3)+'_'+tres+'min_l2_v03.dat'
			url.append(website + f)

			doy = doy + 1

	elif nyears == 2:

		year = year1
		doy = doy1
		while doy <= 365:

			#doytmp = str(doy.astype('S3'))
			website = 'http://www2.physik.uni-kiel.de/stereo/data/sept/level2/'+st+'/'+tres+'min/'+str(year)+'/'
			f = 'sept_'+st+'_ion_omni_'+str(year)+'_'+str(doy).zfill(3)+'_'+tres+'min_l2_v03.dat'
			url.append(website + f)

			doy = doy + 1

		year = year + 1
		doy = 1

		while doy <= doy2:

			#doytmp = str(doy.astype('S3'))
			website = 'http://www2.physik.uni-kiel.de/stereo/data/sept/level2/'+st+'/'+tres+'min/'+str(year)+'/'
			f = 'sept_'+st+'_ion_omni_'+str(year)+'_'+str(doy).zfill(3)+'_'+tres+'min_l2_v03.dat'
			url.append(website + f)


		url.append(website + f)

	else:
		print "Time range spans too many years"


	return url


def date2doy(date):

	"""Determine the DOY for an input date. Input format for date is e.g. '18-aug-2010 00:00 \n'"""

	try: 
		year = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").year 
		month = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").month
		day = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").day

		doy0 = datetime.datetime(year, 1, 1)
		doy = datetime.datetime(year, month, day) - doy0 + datetime.timedelta(days = 1)

		return doy.days

	except:
		print "Enter valid date format e.g. '18-aug-2010 00:00'"

		return None
	




