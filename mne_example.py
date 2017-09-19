#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:09:15 2017

@author: nkoussis
"""

dirname = "/Users/nkoussis/Dropbox/Science/3/PVB304/Article/P001/Brainvision/"
name = "NKoussis_P002_2017-09-12_16-24-31.vhdr"
fname = dirname + name
mname = "standard-10-5-cap385"


 ## Import the relevant libraries

import mne
import scipy
import numpy as np
import matplotlib.pyplot as plt
import mne_fun as fun


 ## Read the raw file

montage = mne.channels.read_montage(mname, path=dirname)
raw = mne.io.read_raw_brainvision(fname, preload=True, montage=montage, eog=['EOG']) 
#see http://martinos.org/mne/stable/python_reference.html#reading-raw-data 
#for more info on how to read eeg data into the program

print(raw)
print(raw.info)
print(raw.ch_names)

 ### Preprocessing for speed (may not be needed)

#tmin, tmax = 20, 200
#raw.crop(tmin, tmax).load_data()  # 20s to 200s data segment for speed
#raw.plot(show_options=True) #plot of raw data
#uncomment if you wish to trim the data

 ### Designating bad channels

 #bad channels
raw.info['bads'] = [] #input your own bad channels here
picks = mne.pick_types(raw.info, meg=False, eeg=True, 
                       eog=True, stim=False,
                       exclude='bads') # setting for eeg data, will have 
                                       #to change values to other
                                       #values for any other types 
                                       #of data to True.

 ### Sensor mapping

raw.plot_sensors() #plotting the sensor map in 2d
raw.plot_sensors(kind='3d', ch_type='eeg', ch_groups='position') #sensor map in 3d


 ### Projection mapping

mne.set_eeg_reference(raw) #prevent MNE from setting reference automatically


 ### Power plot

raw.plot_psd(average=False)


 ### Filtering of data

raw.filter(1, 55, n_jobs=1) #band-pass filter at 55 Hz 
#(set your own frequencies here if you prefer something else)
raw.notch_filter(freqs=[50,100], picks=picks, 
                 filter_length='auto', phase='zero', n_jobs=1) # run cell twice

#plot the power spectral density and the raw data to see what it looks like now
raw.plot_psd(average=False)
raw.plot()

 ### Finding events

events = mne.find_events(raw, stim_channel='STI 014', shortest_event=1)
event_id = {'lett' : 100, 'vis' : 10} #define your own events here
mne.write_events(event_list=events, filename="%s-eve.fif" %name)

 ### Event visualisation

#Plot the events to get an idea of the paradigm
 #Specify colors
color = {10: 'green', 100: 'yellow'}

#mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp, color=color,
                    #event_id=event_id)


 ### Setting epoch parameters

baseline = (None, 0)  # means from the first instant to t = 0
reject = dict(eeg=200e-6) # reject any environmental interference from the epoch


 ### Defining epochs and evoked responses for each trigger

 ### Visual trigger

 #event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                  baseline=baseline, preload=True, reject=reject)
epochs.resample(150, npad='auto', n_jobs=1)
epochs.drop_bad()
evoked_vis = epochs['vis'].average()
evoked_vis.plot(titles='Visual (flashing) feedback evoked response', 
                spatial_colors=True, gfp=True) 
#Plotting evoked response of visual channels

mne.write_evokeds(evoked=evoked_vis, fname="%s_vis-ave.fif" %name)

 #### More visualisation

evoked_vis.plot_topomap(times=np.arange(-0.1, 0.4, 0.05))
ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)

evoked_vis.plot_joint(title='Visual evoked response', 
                      times = [.0, 0.075, 0.125, 0.25],
                      ts_args=ts_args, topomap_args=topomap_args)


 ### "Letter"  inhibition trigger

tmin = -0.5  # start of each epoch (200ms before the trigger)
tmax = 1  # end of each epoch (1000ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, 
                    proj=True, picks=picks,
                    baseline=baseline, preload=True, reject=reject)
epochs.resample(150, npad='auto', n_jobs=1)
epochs.drop_bad()
evoked_lett = epochs['lett'].average()
evoked_lett.plot(titles='Button go/nogo evoked response', 
                 spatial_colors=True, gfp=True)

mne.write_evokeds(evoked=evoked_vis, fname="%s_lett-ave.fif" %name)

evoked_lett.plot_joint(title='Button go/nogo evoked response', 
                       times = np.arange(-0.4, 1, 0.2),
                      ts_args=ts_args, topomap_args=topomap_args)