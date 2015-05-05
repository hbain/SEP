# Solar Energetic Particle Routines

Routines to read particle, magnetic field and solar wind data during solar energetic particle events from instruments on STEREO and ACE.

All routines take date range input in the format

	t1 = '17-jul-2012 00:00'
	t2 = '23-jul-2012 00:00'

## Earth

### omni_range.py

Read and plot the OMNI solar wind (pt, pn, pv)  and IMF (|B|, Bx, By, Bz) data stored in text files previously downloaded from http://omniweb.gsfc.nasa.gov. 
Hourly data files can currently be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/omni/

	import omni as om

	om_dates, B, sw = om.rd_omni(t1, t2)

### protons_range_epam.py**

Read the ACE EPAM protons from text files that were previously downloaded (Not sure of the original source, I got them from a colleague. I'll find out...)
5 min data files can be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/EPAM/

	import protons_range_epam as pre

	epam_dates0, epam_lcurve = pre.parse_epam_proton_range(t1, t2)


## STEREO

### plastic_range.py

Read and plot the STEREO PLASTIC data (solar wind density, temperature, velocity). Reads the data from http://stereo-ssc.nascom.nasa.gov/data/ins_data/plastic/level2/Protons/ASCII/... The exact URL of the data is determined through input arguements to routine i.e. start time, end time, spacecraft (A or B) and temporal resolution. 

	import plastic_range as pl

	pla_dates0_a, pla_n_a, pla_v_a, pla_t_a = pl.parse_plastic_range(t1, t2, 'a', 1)


### mag_range.py
Read and plot the STEREO MAG data (Br, Bt, Bn, B, Blat, Blon)

STEREO MAG ASCII files created here: http://aten.igpp.ucla.edu/forms/stereo/level2_plasma_and_magnetic_field.html

Example of 1 minute time resolution files can be found here: http://sprg.ssl.berkeley.edu/~hbain/sep_data/MAG/

	import mag_range as mg

	mag_dates0_a, Br_a, Bt_a, Bn_a, B_a, Blat_a, Blon_a = mg.parse_mag_range(t1,t2, 'a', 1)



### protons_range.py

Read and plot the STEREO proton data from the SEPT, LET and HET instruments (might not cover the full energy ranges possible - I may have only picked those I needed). 

SEPT data is here: http://www2.physik.uni-kiel.de/stereo/data/sept/level2/

HET data is here: http://www.srl.caltech.edu/STEREO/DATA/HET/

LET data is here: http://www.srl.caltech.edu/STEREO/DATA/Level1/Public/ahead/1Minute/

The exact URL of the data is determined through input arguements to routine i.e. start time, end time, spacecraft (A or B) and temporal resolution. 


	import protons_range as pr

	sept_dates0, sept_lcurve = sept_proton_lcurve_range(t1, t2, stereo, '1')

	let_sum_dates0_a, let_sum_lcurve_a = pr.parse_let_proton_range(t1, t2, 'a', '1')

	het_sum_dates0_a, het_sum_lcurve_a = pr.het_proton_lcurve_range(t1, t2, 'a', '1')



## Shocks 

### rd_shocks_xls.py

Check for shock passages at the STEREO spacecraft, using the identified shock list compiled by Lan Jian
http://www-ssc.igpp.ucla.edu/forms/stereo/stereo_level_3.html

Currently the identified shocks are saved as a text file STEREO_Level3_Shock2.xls

	import rd_shocks_xls as shks

	tshock_sta, tshock_stb = shks.stereo_shock()			#read in list of shocks

	tsa = shks.time_in_range(t1, t2, tshock_sta, dtfmt=1) 

	tsb = shks.time_in_range(t1, t2, tshock_stb, dtfmt=1) 

### rd_ace_shocks.py

Check for shock passages at the ACE spacecraft, using the identified shock list compiled at the CfA https://www.cfa.harvard.edu/shocks/ac_master_data/ac_master_2010.html

Currently the identified shocks are saved as a text file ace_shocks.txt

	import rd_ace_shocks as ashks

	ash = ashks.rd_ace_shocks()

	tse = ashks.time_in_range(t1, t2, ash, dtfmt=1)

