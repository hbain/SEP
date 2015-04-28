


from datetime import datetime, timedelta
import numpy as np


def plot_omni(t1, t2):

	"""TODO: plot the OMNI solar win and IMF data """




def rd_omni(t1, t2):

	"""REad the OMNI solar wind and IMF data"""

	year = '2012'

	fname = '/Users/hazelbain/Dropbox/sep_archive/omni/omni2_'+year+'.dat.txt'

	#column names in omni data file (variables "v" need to be named correctly)
	name = ('year', 'doy', 'hour', 'v3', 'v4', 'v5', 'v6', 'v7', 'b', 'v9', 'v10', 'v11', 'bx', 'by', 'bz', 'v15', 'v16', 'v17', 'v18', 'v19', 'v20', 'v21', \
	'pt', 'pn', 'pv', 'v25', 'v26', 'v27', 'v28', 'v29', 'v30', 'v31', 'v32', 'v33', 'v34', 'v35', 'v36', 'v37', 'v38', 'v39', 'v40','v41', 'v42', 'v43', 'v44', 'v45', 'v46',\
	'v47', 'v48','v49', 'v50','v51', 'v52','v53', 'v54' )

	#data format for each column
	form = ('i4', 'i4', 'i4', 'i4', 'i4', 'i4', 'i4', 'i4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'i4', \
	'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'i4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'i4', 'i4', 'i4', 'i4','f4', 'f4', 'f4', 'f4', 'f4', 'f4',\
	'i4', 'i4','f4', 'f4','i4', 'i4','f4' )

	#load data into np array
	data = np.loadtxt(fname, dtype =  {'names': name, 'formats': form})

	#get the data times
	time = []
	for i in range(len(data)): 
		time_tmp = datetime(data['year'][i], 1, 1) + timedelta(data['doy'][i] - 1) 
		time.append(time_tmp + timedelta(hours = int((data['hour'][i]))))
	time = np.asarray(time)


	#(|B|, Bz, By, Bz)
	B = data[['b', 'bx', 'by', 'bz']]

	#solar wind (pt, pn, pv)
	sw = data[['pt', 'pn', 'pv']]

	return time, B, sw
