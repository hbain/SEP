import numpy as np
from urllib2 import urlopen
from StringIO import StringIO
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties
from dateutil.relativedelta import relativedelta
import math
import platform

def make_mag_plots_range(t1, t2, stereo):
	
	year1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").year 
	month1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").month 
	day1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").day
	
	#convert to datetime format
	dt1 = datetime.datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.datetime.strptime(t2, "%d-%b-%Y %H:%M")
	ndays = (dt2 - dt1).days

	#parse the STEREO MAG 
	mag_dates0, Br, Bt, Bn, B, Blat, Blon = parse_mag_range(t1,t2, stereo)

	if mag_dates0 is not None:

		#determing y axis range on the good data only
		Br_high = yrange_fix(Br)
		Bt_high = yrange_fix(Bt)
		Bn_high = yrange_fix(Bn)
		B_high = yrange_fix(B)

		#set up 1x3 figure
		f, (ax0, ax1, ax2, ax3) = plt.subplots(4, 1)
		#plt.subplots_adjust(hspace=0.5) # increase the distances between subplots
		#plt.subplots_adjust(wspace=0.5)

		#legend
		fontP = FontProperties()
		fontP.set_size('x-small')

		#B RTN
		ax0.plot(mag_dates0, Br, label='Br', color='r')
		ax0.plot(mag_dates0, Bt, label='Bt', color='b')
		ax0.plot(mag_dates0, Bn, label='Bn', color='g')
		hrsFmt = mdates.DateFormatter('%d')
		ax0.xaxis.set_major_formatter(hrsFmt)
		f.autofmt_xdate()
		#ax0.set_yscale('log')
		yr = max(np.array([max(Br_high, Bt_high, Bn_high), abs(min(np.concatenate([Br, Bt, Bn])))]))
		ax0.set_ylim(top = yr)
		ax0.set_ylim(bottom = -yr)
		ax0.set_title('MAG ST'+stereo.capitalize())
		ax0.set_ylabel('$\mathrm{B_{R,T,N} (nT)}$')
		ax0.set_xlabel("Start Time "+mag_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
		leg = ax0.legend(loc='best', prop = fontP, fancybox=True )

		#|B|
		ax1.plot(mag_dates0, B, label='|B|')
		hrsFmt = mdates.DateFormatter('%d')
		ax1.xaxis.set_major_formatter(hrsFmt)
		f.autofmt_xdate()
		#ax1.set_yscale('log')
		ax1.set_ylim(top = B_high)
		ax1.set_ylabel('|B| (nT)')
		ax1.set_xlabel("Start Time "+mag_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
		leg = ax1.legend(loc='best', prop = fontP, fancybox=True )

		#Blat
		ax2.plot(mag_dates0, Blat, label='B lat', color='black', marker='o', markersize = 1, linestyle ='None')
		hrsFmt = mdates.DateFormatter('%d')
		ax2.xaxis.set_major_formatter(hrsFmt)
		f.autofmt_xdate()
		#ax1.set_yscale('log')
		#ax1.set_ylim(top = B_high)
		ax2.set_ylabel('$\mathrm{B lat (^{o})}$')
		ax2.set_xlabel("Start Time "+mag_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
		leg = ax2.legend(loc='best', prop = fontP, fancybox=True )

		#Blon
		ax3.plot(mag_dates0, Blon, label='B lon', color='black', marker = 'o', markersize = 1, linestyle ='None')
		hrsFmt = mdates.DateFormatter('%d')
		ax3.xaxis.set_major_formatter(hrsFmt)
		f.autofmt_xdate()
		#ax1.set_yscale('log')
		ax3.set_ylim(top = 360)
		ax3.set_ylim(bottom = 0)
		ax3.set_ylabel('$\mathrm{B lon (^{o})}$')
		ax3.set_xlabel("Start Time "+mag_dates0[0].strftime("%d-%b-%Y %H:%M")+" (UTC)")
		leg = ax3.legend(loc='best', prop = fontP, fancybox=True )

		plt.show()
		#plt.savefig('plots/mag_range/ST'+stereo.capitalize()+'_mag_'+str(year1)+str(month1).zfill(2)+str(day1).zfill(2)+'_'+str(ndays)+'.jpeg', format='jpeg')


	return None

def parse_mag_range(t1, t2, stereo, tres):

	"""Read in STEREO MAG data (Br, Bt, Bn, B, Blat, Blon)"""

	#Read in data from local dat file
	year1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").year 
	month1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").month 
	day1 = datetime.datetime.strptime(t1,"%d-%b-%Y %H:%M").day
	
	year2 = datetime.datetime.strptime(t2,"%d-%b-%Y %H:%M").year 
	month2 = datetime.datetime.strptime(t2,"%d-%b-%Y %H:%M").month 
	day2 = datetime.datetime.strptime(t2,"%d-%b-%Y %H:%M").day

	if tres == 1:		# 1 minute resolution

		#which computer am I using, what path should I use to save the data
		if platform.platform()[0:3] == 'Dar':
			dd = '/Users/hazelbain/'
		elif platform.platform()[0:3] == 'Lin':
			dd = '/home/hbain/'

		#if the desired time range stretches over 2 months, then concatenate the files
		#-----this needs some work to extend data parsing to longer periods of time------ 
		if month1 == month2:

			##MAG ASCII files created here: http://aten.igpp.ucla.edu/forms/stereo/level2_plasma_and_magnetic_field.html
			##Example of 1 minute time resolution files can be found here: http://sprg.ssl.berkeley.edu/~hbain/sep_data/MAG/
			file = dd + 'Dropbox/sep_archive/mag_txt/mag_month_1min/st'+stereo+'_mag_'+str(year1)+'_'+str(month1).zfill(2)+'_1min.txt'
			txt = open(file, 'r').read()
			body = txt.split('DATA:\n')[1].split('\n')	
			data = np.loadtxt(body)
			#txt.close()
		elif month1 == month2 - 1:
			file = dd + 'Dropbox/sep_archive/mag_txt/mag_month_1min/st'+stereo+'_mag_'+str(year1)+'_'+str(month1).zfill(2)+'_1min.txt'
			txt = open(file, 'r').read()
			body = txt.split('DATA:\n')[1].split('\n')	
			data_tmp1 = np.loadtxt(body)
			#txt.close()

			file = dd + 'Dropbox/sep_archive/mag_txt/mag_month_1min/st'+stereo+'_mag_'+str(year1)+'_'+str(month2).zfill(2)+'_1min.txt'
			txt = open(file, 'r').read()
			body = txt.split('DATA:\n')[1].split('\n')	
			data_tmp2 = np.loadtxt(body)

			data = np.concatenate([data_tmp1, data_tmp2], axis = 0)


	elif tres == 10:			#10 minute resolution

		#if the desired time range stretches over 2 months, then concatenate the files
		#-----this needs some work to extend data parsing to longer periods of time------ 
		if month1 == month2:
			file =  dd+ 'Dropbox/sep_archive/mag_txt/st'+stereo+'_mag_'+str(year1)+'_'+str(month1).zfill(2)+'.dat'
			txt = open(file, 'r').read()
			body = txt.split('DATA:\n')[1].split('\n')	
			data = np.loadtxt(body)
			#txt.close()
		elif month1 == month2-1:
			file = dd + 'Dropbox/sep_archive/mag_txt/st'+stereo+'_mag_'+str(year1)+'_'+str(month1).zfill(2)+'.dat'
			txt = open(file, 'r').read()
			body = txt.split('DATA:\n')[1].split('\n')	
			data_tmp1 = np.loadtxt(body)

			file = dd + 'Dropbox/sep_archive/mag_txt/st'+stereo+'_mag_'+str(year1)+'_'+str(month2).zfill(2)+'.dat'
			txt = open(file, 'r').read()
			body = txt.split('DATA:\n')[1].split('\n')	
			data_tmp2 = np.loadtxt(body)

			data = np.concatenate([data_tmp1, data_tmp2], axis = 0)


	else: 
		"No such temporal resolution for MAG"


	# mn = month1
	# data = np.ndarray([])
	# while mn <= month2:
	# 	#file = '/Users/hazelbain/Dropbox/sep_archive/a4773.dat'
	# 	file = '/Users/hazelbain/Dropbox/sep_archive/mag_txt/st'+stereo+'_mag_'+str(year1)+'_'+str(mn).zfill(2)+'.dat'

	# 	txt = open(file, 'r').read()
	# 	body = txt.split('DATA:\n')[1].split('\n')	
	# 	data_temp = np.loadtxt(body)

	# 	#concatenate data files
	# 	if data.size == 1:
	# 		data = data_temp
	# 	else:
	# 		data = np.concatenate([data, data_temp])

	# 	#advance months
	# 	if mn != 12:
	# 		mn = mn + 1
	# 	else:
	# 		mn = 1
	# 		year1 = year1 + 1

	#extract just the data corresponding to the specified time range
	sw = np.min(np.where(np.logical_and(data[:,1] == month1, data[:,2] == day1))[0])
	ew = np.max(np.where(np.logical_and(data[:,1] == month2, data[:,2] == day2))[0])

	#make sure the end index is greater than the start index
	if ew > sw:

		data2 = data[sw:ew+1, :]

		#Time axis
		year0 = int(data2[0][0])
		month0 = int(data2[0][1])
		day0 = int(data2[0][2])
		hour0 = int(data2[0][3])
		mins0 = int(data2[0][4])

		base0 = datetime.datetime(year0, month0, day0, hour0, mins0) 
			
		dates0 = []
		for x in range(0,len(data2)):
			dates0.append(datetime.datetime(int(data2[x,0]), int(data2[x,1]), int(data2[x,2]), int(data2[x,3]), int(data2[x,4])))
				
		#MAG data
		Br = data2[:,7]
		Bt = data2[:,8]
		Bn = data2[:,9]
		B = data2[:,10]

		#calc Blon and Blat			---- need to check this calc is correct. Leske et (2012)
		Blat = np.degrees(np.arcsin(Bn/B))
		if stereo == 'a':
			Blon = np.degrees(np.arctan2(-Bt, Br)) 
		elif stereo == 'b':
			Blon = np.degrees(np.arctan2(-Bt, Br)) 
		else:
			"No such instrument"
		wneg = np.where(Blon < 0.)
		Blon[wneg] = Blon[wneg] + 360.

		return dates0, Br, Bt, Bn, B, Blat, Blon

	else:
		
		return None

def yrange_fix(x):
	"""Check for missing data in the array. Will have a value of 0.1e35"""

	w = np.where(x != 0.1e35)
	xvalid = x[w]
	yhigh = max(xvalid) 

	return yhigh



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
    args = parser.parse_args()

    result = make_mag_plots_range(args.t1, args.t2, args.stereo)

   









