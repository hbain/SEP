import xlrd
import numpy as np
from datetime import datetime
import platform


def stereo_shock():

	"""REads in the complete list of shocks observed at STEREO - use time_in_range to determine if there
	is a shock passage in the time period of interest.

	List complied at Lan Jian http://www-ssc.igpp.ucla.edu/forms/stereo/stereo_level_3.html

	"""

	if platform.platform()[0:3] == 'Dar':
		dd = '/Users/hazelbain/'
	elif platform.platform()[0:3] == 'Lin':
		dd = '/home/hbain/'

	filename = dd + 'Dropbox/sep_archive/STEREO_Level3_Shock2.xls'

	wb = xlrd.open_workbook(filename)		#open
	sh = wb.sheet_by_index(0)				#get the first sheet


	#split data into STA and STB
	col0 = np.asarray(sh.col_values(0))
	w1 = np.where(col0 == '1.0')			#start indices for shocks

	st_sta = w1[0][0]
	et_sta = np.where(col0 == 'Interplanetary  Shocks  at  STEREO B')[0][0]-2

	st_stb = w1[0][1]
	et_stb = np.where(col0 == '1 Bdown/Bup: ratio of downstream magnetic field intensity to upstream magnetic field intensity')[0][0]-3


	data_sta = np.asarray([sh.col_values(1), sh.col_values(2), sh.col_values(3), sh.col_values(4), sh.col_values(5), sh.col_values(6)])[:,st_sta:et_sta+1]
	data_stb = np.asarray([sh.col_values(1), sh.col_values(2), sh.col_values(3), sh.col_values(4), sh.col_values(5), sh.col_values(6)])[:,st_stb:et_stb+1]

	nevents_a = len(data_sta[0])
	nevents_b = len(data_stb[0])

	tshock_sta = []
	for i in range(nevents_a): tshock_sta.append(datetime(int(float(data_sta[0,i])), int(float(data_sta[1,i])), int(float(data_sta[2,i])), int(float(data_sta[3,i])), int(float(data_sta[4,i])), int(float(data_sta[5,i]))))

	tshock_stb = []
	for i in range(nevents_b): tshock_stb.append(datetime(int(float(data_stb[0,i])), int(float(data_stb[1,i])), int(float(data_stb[2,i])), int(float(data_stb[3,i])), int(float(data_stb[4,i])), int(float(data_stb[5,i]))))


	return tshock_sta, tshock_stb


def time_in_range(t1, t2, x, dtfmt=0):
	"""Return true if array of times x is in the range [t1, t2]"""

	dt1 = datetime.strptime(t1, "%d-%b-%Y %H:%M")
	dt2 = datetime.strptime(t2, "%d-%b-%Y %H:%M")
	nt = len(x)

	t_in = []
	for i in range(nt):
		if dt1 <= dt2:
			if dt1 <= x[i] <= dt2:

				if dtfmt == 1:
					t_in.append(x[i])

				else:
					t_in.append(datetime.strftime(x[i], "%d-%b-%Y %H:%M"))

		else:
			dt1<= x[i] or x[i] <= dt2

	return t_in












