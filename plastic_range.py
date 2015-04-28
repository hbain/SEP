import numpy as np
from urllib2 import urlopen
from StringIO import StringIO
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties
from dateutil.relativedelta import relativedelta


def make_plastic_plots_range(t1, t2, stereo, tres):

	#convert times to datetime format
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")

	#LET 1.8 - 10 MeV protons
	pla_dates0, pla_n, pla_v, pla_t = parse_plastic_range(t1, t2, stereo, tres)

	nhigh = yrange_fix(pla_n)
	vhigh = yrange_fix(pla_v)
	thigh = yrange_fix(pla_t)

	#set up 1x3 figure
	f, (ax0, ax1, ax2) = plt.subplots(3, 1)
	#plt.subplots_adjust(hspace=0.5) # increase the distances between subplots
	#plt.subplots_adjust(wspace=0.5)

	#legend for plot
	fontP = FontProperties()
	fontP.set_size('x-small')

	#Proton velocity
	ax0.plot(pla_dates0, pla_v, label='Proton velocity')
	hrsFmt = mdates.DateFormatter('%d')
	ax0.xaxis.set_major_formatter(hrsFmt)
	f.autofmt_xdate()
	#ax0.set_yscale('log')
	ax0.set_ylim(top = vhigh)
	ax0.set_ylim(bottom = min(pla_v))
	ax0.set_title('PLASTIC ST'+stereo.capitalize())
	ax0.set_ylabel('$\mathrm{v\,(km\,s^{-1})}$')
	ax0.set_xlabel("Start Time "+pla_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
	leg = ax0.legend(loc='best', prop = fontP, fancybox=True )

	#Proton density
	ax1.plot(pla_dates0, pla_n, label='Proton density')
	hrsFmt = mdates.DateFormatter('%d')
	ax1.xaxis.set_major_formatter(hrsFmt)
	f.autofmt_xdate()
	ax1.set_yscale('log')
	ax1.set_ylim(top = nhigh)
	ax1.set_ylabel('$\mathrm{n_{p}\,(cm^{-3})}$')
	ax1.set_xlabel("Start Time "+pla_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
	leg = ax1.legend(loc='best', prop = fontP, fancybox=True )

	#Proton temperature
	ax2.plot(pla_dates0, pla_t, label='Proton temperature')
	hrsFmt = mdates.DateFormatter('%d')
	ax2.xaxis.set_major_formatter(hrsFmt)
	f.autofmt_xdate()
	ax2.set_yscale('log')
	ax2.set_ylim(top = thigh)
	ax2.set_ylabel('$\mathrm{T\,(K)}$')
	ax2.set_xlabel("Start Time "+pla_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
	leg = ax2.legend(loc='best', prop = fontP, fancybox=True )

	#leg = ax.legend(loc='best', prop = fontP, fancybox=True )
	#leg.get_frame().set_alpha(0.5)

	##for saving file name
	year1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").year 
	month1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").month 
	day1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").day
	
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")
	ndays = (dt2 - dt1).days

	plt.show()
	#plt.savefig('plots/plastic_range/ST'+stereo.capitalize()+'_plastic_'+str(year1)+str(month1).zfill(2)+str(day1).zfill(2)+'_'+str(ndays)+'.jpeg', format='jpeg')


	return None


def parse_plastic_range(t1, t2, stereo, tres):

	"""Parse STEREO PLASTIC data in time range t1 to t2. 
	Time format should be e.g.'18-aug-2010 01:00' """

	#Read in data from web 
	#determine the URL of the data based on the start time, spacecracft and temporal resolution
	url = fetch_ascii_url_range(t1, t2, stereo, tres)

	#read in data from web
	for i in range(len(url)):
		urlfile = url[i]
		try:
			#remove the header before reading in data
			txt = urlopen(urlfile).read()
			head = txt.split(']\n')[0].split('\t')
			body = txt.split(']\n')[1]
			body2 = body.replace('\t', ' ').replace('/','').replace('-','').replace(':','').split('\n')
			data_temp = np.loadtxt(body2)

			#concatenate files
			if i == 0: 
				data = data_temp
			else: 
				data = np.concatenate([data, data_temp], axis=0)

		except:
			print "Something wrong with PLASTIC file "+urlfile


	#Times/date
	year = int(data[0][0])
	doy = int(data[0][1])
	hour = int(data[0][2])
	mins = int(data[0][3])
	
	dates0 = []
	for x in range(0,len(data)):
		dates0.append(datetime.datetime(year, 1, 1, 0, 0) + datetime.timedelta(days = int(data[x, 1]) - 1, hours = int(data[x, 2]), minutes = int(data[x, 3])))
			
	#PLASTIC density, temperature and velocity measurements
	# v = data[:,9]
	# n = data[:,8]
	# temp = data[:,10]

	n = data[:,5]
	temp = data[:,7]
	v = data[:,6]


	return dates0, n, v, temp

def yrange_fix(x):
	"""Check for missing data in the array. Will have a value of 1.e31"""

	w = np.where(x != 1.e31)
	xvalid = x[w]
	yhigh = max(xvalid) 

	return yhigh


def fetch_ascii_url_range(t1, t2, stereo, res):

	"""Determine the URL of the STEREO PLASTIC txt files between t1 and t2
	with temporal resoultion res.

	t1 = start time in ut format i.e. '18-aug-2010 00:00'
	stereo = 'A' or 'B' for sta/stb
	res = temporal resoluion either 1 or 10 for 1 and 10 minute summed files
	"""


	doy1 = date2doy(t1)
	doy2 = date2doy(t2)
	doy = np.array(np.arange(doy1, doy2+1))
	ndays = len(doy)

	#Temporal resolution
	if res == 1 or 10:
		res = str(res)
	else:
		print "Choose which temporal resolution data to use. 1 or 10"

	#put together the URL	

	url = []
	tt = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M")
	for i in range(ndays):

		#increment the date through the timerange
		year = tt.year 
		month = tt.month
		day = tt.day 

		#construct exact url
		website = 'http://stereo-ssc.nascom.nasa.gov/data/ins_data/plastic/level2/Protons/ASCII/'+res+'min/'+stereo.capitalize()+'/'+str(year)+'/'
		f = 'ST'+stereo.capitalize()+'_L2_PLA_1DMax_'+res+'min_'+str(year)+str(month).zfill(2)+str(day).zfill(2)+'_'+doy.astype('S3')[i].zfill(3)+'_V09.txt'
		url.append(website + f)

		#increment time
		tt =  tt + datetime.timedelta(days=1)

	return url



def date2doy_decimal(date):

	"""Determine the DOY for an input date. Input format for date is e.g. '18-aug-2010 00:00 \n'"""

	try: 
		year = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").year 
		month = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").month
		day = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").day
		hour = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").hour
		minute = datetime.datetime.strptime(date,"%d-%b-%Y %H:%M").minute

		doy0 = datetime.datetime(year, 1, 1)
		doyfrac = ((hour * 60.) + minute) / 1440.
		doy = datetime.datetime(year, month, day) - doy0 + datetime.timedelta(days = 1) 

		return doy.days + doyfrac

	except:
		print "Enter valid date format e.g. '18-aug-2010 00:00'"

		return None

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
	

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('t1', type = str,  help='Starting time for plots')
    parser.add_argument('t2', type = str,  help='Ending time for plots')
    parser.add_argument('stereo', type = str,  help='Which STEREO Spacecraft')
    parser.add_argument('tres', type = str,  help='Temporal Resolution')
   	args = parser.parse_args()

    result = make_plastic_plots_month(args.t1, args.t2, args.stereo, args.tres)

   









