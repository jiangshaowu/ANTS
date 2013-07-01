import os as os
import numpy as np
from obspy.core import read
from obspy.core import trace
import matplotlib.pyplot as plt


#==================================================================================================
# TAPER
#==================================================================================================

def taper(data,width,verbose):

	if verbose==True: print '* taper '+str(100*width)+' percent of trace'
	data.taper('cosine',p=width)

	return data


#==================================================================================================
# DETREND
#==================================================================================================

def detrend(data,verbose):

	if verbose==True: print '* demean and detrend'
	data.detrend('linear')
	data.detrend('demean')

	return data


#==================================================================================================
# BANDPASS FILTER
#==================================================================================================

def bandpass(data,corners,f_min,f_max,verbose):

	if verbose==True: print '* bandpass between '+str(f_min)+' and '+str(f_max)+' Hz'
	data.filter('lowpass',freq=f_max,corners=corners,zerophase=False)
	data.filter('highpass',freq=f_min,corners=corners,zerophase=False)

	return data


#==================================================================================================
# REMOVE INSTRUMENT RESPONSE
#==================================================================================================

def remove_response(data,respdir,unit,verbose):

	"""
	Remove instrument response located in respdir from data. Unit is displacement (DIS), velocity (VEL) or acceleration (ACC).

	Return 1 if successful. Return 0 otherwise.
	"""

	#- RESP file ==================================================================================
	resp_file=respdir+'/RESP.'+data.stats.network+'.'+data.stats.station+'.'+data.stats.location+'.'+data.stats.channel

	if verbose==True: print '* RESP file: '+resp_file

	#- try to remove response if the RESP file exists =============================================

	if os.path.exists(resp_file):

		success=1

		if verbose==True: print '* remove instrument response, unit='+unit
		resp_dict = {"filename": resp_file, "units": unit, "date": data.stats.starttime}

		try:
			data.simulate(seedresp=resp_dict)
		except ValueError:
			if verbose==True: print '* could not find correct RESP file, recording rejected'
			success=0

	#- response cannot be removed because RESP file does not exist

	else:
		if verbose==True: print '* could not find correct RESP file, recording rejected'
		success=0

	return success, data


#==================================================================================================
# DOWNSAMPLING
#==================================================================================================

def downsample(data, Fsnew, verbose):
    
    Fs=float(data.stats.sampling_rate) 
    Fsnew=float(Fsnew)
    
    data_new=data.copy()

	#- check if data already have the desired sampling rate =======================================

    if Fs==Fsnew:
        if verbose==True: 
        	print '* Current and new sampling rate are equal. No downsampling performed.'

	# Downsampling ================================================================================

    else:
    	dec=int(Fs/Fsnew)
    	data_new.decimate(dec, no_filter=True)
    	if verbose==True: 
			print '* Downsampling by factor '+str(dec)

    # Plotting if wanted ==========================================================================

    #if plot==True:
    	#data.plot()
    	#data_new.plot()

    	#t = np.arange(0, data.stats.npts / data.stats.sampling_rate, data.stats.delta)
    	#t_new = np.arange(0, data_new.stats.npts / data_new.stats.sampling_rate, data_new.stats.delta)
    
    	#plt.plot(t[1:20000], data[0].data[1:20000], 'g', label='Raw', alpha=0.9)
    	#plt.plot(t_new[1:20000/dec], data_new[0].data[1:20000/dec], 'r--', label='Downsampled', alpha=0.9)
    
    	#plt.show()
   
   
    return data_new
    
    