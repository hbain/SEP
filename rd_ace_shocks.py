
from datetime import datetime
import numpy as np

def rd_ace_shocks():

	"""REads in the complete list of shocks observed at ACE - use time_in_range to determine if there
	is a shock passage in the time period of interest.
	- list complied at Cfa e.g. https://www.cfa.harvard.edu/shocks/ac_master_data/ac_master_2010.html
	"""

	#read ace shocks text file
	fname = '/Users/hazelbain/Dropbox/sep_archive/ace_shocks.txt'
	dt = {'names': ( 'year', 'month', 'day', 'doy', 'hour', 'minute', 'x', 'y', 'z', 'type' ),
	      'formats': ( 'i4', 'i4', 'i4', 'f4', 'i4', 'i4', 'f4', 'f4', 'f4', 'S2')}

	data = np.loadtxt(fname, dtype = dt )

	#shock time in datetime format
	tshk = []
	for i in range(len(data)): 
		tshk.append(datetime(data[i]['year'], data[i]['month'], data[i]['day'], data[i]['hour'], data[i]['minute']))


	return tshk

def time_in_range(t1, t2, x, dtfmt=0):

	"""Return true if array of times x is in the range [t1, t2]. If dtfmt = 0 return in datetime formate"""

	if type(t1) == str: 

		dt1 = datetime.strptime(t1, "%d-%b-%Y %H:%M")
		dt2 = datetime.strptime(t2, "%d-%b-%Y %H:%M")
	else:
		dt1 = t1
		dt2 = t2
	
	nt = len(x)

	t_in = []
	for i in range(nt):
		if dt1 <= dt2:
			if dt1 <= x[i] <= dt2:

				# if dtfmt = 0 resturn in datetime format
				if dtfmt == 0:
					t_in.append(datetime.strftime(x[i], "%d-%b-%Y %H:%M"))
				#otherwise return as string
				else:
					t_in.append(x[i])


		else:
			continue

	return t_in

