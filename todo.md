# To do

Things to do...in no particular order:

- Check that each routine works for times crossing yearly boudaries i.e. t1 = '20-dec-2010' t2 = '5-jan-2011'. Should work for some of the routines.

- Add functionality to include different time resolutions, particularly for ACE EPAM and OMNI

- Add functionality to read in different species. Currenly only works for protons, but this could just be added as an arguement in the call as it just changes the URL that you go to. Though data file format may change, especially since the energy ranges will be different for Ions. 

- Read the data in to Pandas arrays? Currently data is just in a numpy array. 

- Write some code to query the OMNI, STEREO MAG, ACE EPAM web servers for the data instead of reading from text files which have to be downloaded by the user prior to running the routines.