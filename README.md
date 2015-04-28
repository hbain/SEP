# SEP
Routines to read particle, magnetic field and solar wind data during solar energetic particle events from instruments on STEREO and ACE.


- omni_range.py 
Read and plot the OMNI solar wind (pt, pn, pv)  and IMF (|B|, Bx, By, Bz) data stored in text files previously downloaded from http://omniweb.gsfc.nasa.gov. 
Hourly data files can currently be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/omni/

- protons_range_epam.py 
Read the ACE EPAM protons from text files that were previously downloaded (Not sure of the original source, I got them from a colleague. I'll find out...)
5 min data files can be found at http://sprg.ssl.berkeley.edu/~hbain/sep_data/EPAM/
