# SEP
Routines to read particle, magnetic field and solar wind data during solar energetic particle events from instruments on STEREO and ACE.

All routines take date range input in the format

	t1 = '17-jul-2012 00:00'
	t2 = '23-jul-2012 00:00'

- omni_range.py 
Read and plot the OMNI solar wind (pt, pn, pv)  and IMF (|B|, Bx, By, Bz) data stored in text files previously downloaded from http://omniweb.gsfc.nasa.gov. 
Hourly data files can currently be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/omni/

import omni as om
om_dates, B, sw = om.rd_omni(t1, t2)

- protons_range_epam.py 
Read the ACE EPAM protons from text files that were previously downloaded (Not sure of the original source, I got them from a colleague. I'll find out...)
5 min data files can be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/EPAM/

import protons_range_epam as pre
epam_dates0, epam_lcurve = pre.parse_epam_proton_range(t1, t2)


STEREO

- plastic_range.py 
Read and plot the STEREO PLASTIC data (solar wind density, temperature, velocity). Reads the data from http://stereo-ssc.nascom.nasa.gov/data/ins_data/plastic/level2/Protons/ASCII/... The exact URL of the data is determined through input arguements to routine i.e. start time, end time, spacecraft (A or B) and temporal resolution. 