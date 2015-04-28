import numpy as np
from StringIO import StringIO
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties
from dateutil.relativedelta import relativedelta

def plot_epam_proton_lcurves(t1, t2):
	
	#convert time to datetime format
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")

	#set up figure
	nl = 3
	xc = 255/nl
	f, ax = plt.subplots(figsize=(8,4))
	
	#ACE EPAM protons
	epam_dates0, epam_lcurve = parse_epam_proton_range(t1, t2)
	mxepam = np.amax(epam_lcurve)

	l1 = ax.plot(epam_dates0, epam_lcurve[:,0], c = cm.rainbow(1 * xc + 1) ,label='EPAM 0.540 - 0.765 MeV')
	l2 = ax.plot(epam_dates0, epam_lcurve[:,1], c = cm.rainbow(3 * xc + 1) ,label='EPAM 0.765 - 1.22 MeV')
	l3 = ax.plot(epam_dates0, epam_lcurve[:,2], c = cm.rainbow(5 * xc + 1) ,label='EPAM 1.22 - 4.94 MeV')
		
	#format of tick labels
	hrsFmt = mdates.DateFormatter('%d')
	ax.xaxis.set_major_formatter(hrsFmt)
	ax.set_xlabel("Start Time "+t1+" (UTC)")
	ax.set_xlim([dt1, dt2])
	ymax = np.max([mxepam, mxepam])
	ax.set_ylim(top = ymax)
	ax.set_ylim(bottom = 1.e-4)

	#auto orientate the labels so they don't overlap
	#f.autofmt_xdate()

	#set yaxis log
	ax.set_yscale('log')

	#Axes labels
	ax.set_title("ACE EPAM Protons")
	ax.set_ylabel('H Intensity $\mathrm{(cm^{2}\,sr\,s\,MeV)^{-1}}$')

	#legend
	fontP = FontProperties()
	fontP.set_size('x-small')

	leg = ax.legend(loc='best', prop = fontP, fancybox=True )
	leg.get_frame().set_alpha(0.5)

	#month
	year = dt1.year
	month = dt1.month

	plt.show()
	
	return None


def parse_epam_proton_range(t1, t2):

	"""Parse ACE EPAM protons"""

	#convert to datetime format
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")

	year = dt1.year

	#Read in data from txt file - data can be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/EPAM/
	fname = "/Users/hazelbain/Dropbox/sep_archive/yan_monthly_sep_plots/ACE_EPAM"+str(year)+"fpe_5min.txt"

	try:
			
		f = open(fname, 'r')
		datatmp = f.read()
		f.close()
		ss = StringIO(datatmp.split('BEGIN DATA\n')[1])	
		data = np.loadtxt(ss)

	except:
		print "Something wrong with ACE EPAM file " + website + files[i]


	#Read the time/date
	year = int(data[0][0])
	doy = int(data[0][1])
	hour = int(data[0][2])
	mins = int(data[0][3])
	secs = int(data[0][4])
	
	dates0 = []
	for x in range(0,len(data)):
		dates0.append(datetime.datetime(year, 1, 1, 0, 0) + datetime.timedelta(days = int(data[x, 1]) - 1, hours = int(data[x, 2]), minutes = int(data[x, 3]), seconds = int(data[x, 4])))
	dates0 = np.asarray(dates0)

	#trim the data to the start and end times
	wst = np.min(np.where(dates0 >= dt1))
	wet = np.max(np.where(dates0 <= dt2)) +1

	dates0_shrt = dates0[wst:wet]

	#ACE EPAM lightcurve
	epam1 = data[wst:wet, 11]		#FP5:     LEFS150 ,(0.540-0.765 MeV Ions),Sector Avg,1/(cm**2-s-sr-MeV).
	epam2 = data[wst:wet, 12]		#FP6:     LEFS150 ,(0.765-1.22 MeV Ions),Sector Avg,1/(cm**2-s-sr-MeV).
	epam3 = data[wst:wet, 13]		#FP7:     LEFS150 ,(1.22-4.94 MeV Ions),Sector Avg,1/(cm**2-s-sr-MeV).

	#concatenate into structure to return
	epam_lcurve = np.concatenate([[epam1], [epam2], [epam3]], axis = 0).T


	return dates0_shrt, epam_lcurve




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
	




