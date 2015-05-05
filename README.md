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

import plastic_range as pl

pla_dates0_a, pla_n_a, pla_v_a, pla_t_a = pl.parse_plastic_range(t1, t2, 'a', 1)


- mag_range.py
Read and plot the STEREO MAG data (Br, Bt, Bn, B, Blat, Blon)
STEREO MAG ASCII files created here: http://aten.igpp.ucla.edu/forms/stereo/level2_plasma_and_magnetic_field.html
Example of 1 minute time resolution files can be found here: http://sprg.ssl.berkeley.edu/~hbain/sep_data/MAG/
