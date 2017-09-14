
# coding: utf-8

# #### --coding: utf-8--

# ## Import the data

# In[1]:

import Tkinter
import tkFileDialog
root = Tkinter.Tk()
fname = tkFileDialog.askopenfilename(parent=root, initialdir='/users/nikitaskoussis/Dropbox/Science/PVB304/Article/MNE', 
                                    title='Please select your EEG file')
root.destroy()


# ## Import the relevant libraries

# In[2]:

import mne
import scipy
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')


# ## Read the raw file

# In[3]:

raw = mne.io.read_raw_eeglab(fname)
print(raw)
print(raw.info)


# In[4]:

print(raw.ch_names)


# ### Preprocessing for speed (may not be needed)

# In[5]:

#tmin, tmax = 20, 200
#raw.crop(tmin, tmax).load_data()  # 20s to 200s data segment for speed
#raw.plot(show_options=True) #plot of raw data


# ### Designating bad channels

# In[4]:

# bad channels
raw.info['bads'] = ['REF','E82','E102','E103','E111','E112','E113','E120','E121',
                    'E122','E123','E124','E133','E134','E135','E136','E145','E146',
                    'E147','E156','E167','E210','E229','E237','E256']
picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False,
                       exclude='bads')


# ### Sensor mapping

# In[5]:

raw.plot_sensors() #plotting the sensor map in 2d
raw.plot_sensors(kind='3d', ch_type='eeg', ch_groups='position') #sensor map in 3d


# ### Projection mapping

# In[6]:

mne.set_eeg_reference(raw) #prevent MNE from setting reference automatically


# ### Power plot

# In[9]:

raw.plot_psd(average=False)


# ### Filtering of data

# In[8]:

raw.filter(l_freq=None, h_freq=55) #low-pass filter at 55 Hz so auditory triggers aren't cut off
raw.filter(l_freq=1, h_freq=None) #high-pass filter at 1 Hz
raw.notch_filter(freqs=[50,100], picks=picks, filter_length='auto', phase='zero') # run cell twice


# In[9]:

raw.plot_psd(average=False)
raw.plot()


# ### Finding events

# In[10]:

events = mne.find_events(raw, stim_channel='STI 014', shortest_event=1)
event_id = {'lett' : 110, 'aud_l' : 137, 'aud_r' : 138, 'vis_l' : 87, 'vis_r' : 88}
print(event_id)
mne.write_events(event_list=events, filename='loc_out_noepi-eve.fif')


# ### Event visualisation

# In[11]:

# Plot the events to get an idea of the paradigm
# Specify colors
color = {87: 'green', 138: 'yellow', 137: 'red', 110: 'black', 88: 'c'}

mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp, color=color,
                    event_id=event_id)


# ### Setting baseline

# In[12]:

baseline = (None, 0)  # means from the first instant to t = 0


# ### Peak-to-peak rejection parameters

# In[13]:

reject = dict(eeg=200e-6)


# ### Defining epochs and evoked responses for each trigger

# ### Visual trigger

# In[14]:

# event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                  baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
epochs_vis_l = epochs.pick_channels(['E9','E45','E186','E8','E17','E24',
                                  'E43','E52','E53','E80','E90','E81','E132','E157','E148',
                                'E137','E125','E149','E116']) #Setting channels for 
                                          #evoked response of Visual trigger
evoked_vis_l = epochs['vis_l'].average()
evoked_vis_l.plot(titles='Visual (flashing left) feedback evoked response', spatial_colors=True, gfp=True) 
#Plotting evoked response of visual channels


# In[15]:

mne.write_evokeds(evoked=evoked_vis_l,fname='loc_out_noepi_vis_l-ave.fif')


# #### More visualisation

# In[16]:

evoked_vis_l.plot_topomap(times=np.arange(-0.1, 0.4, 0.05))
ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)

evoked_vis_l.plot_joint(title='Visual (flashing left) evoked response', times = [.0, 0.075, 0.125, 0.25],
                      ts_args=ts_args, topomap_args=topomap_args)


# In[18]:

# event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                   baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
epochs_vis_r = epochs.pick_channels(['E9','E45','E186','E8','E17','E24',
                                   'E43','E52','E53','E80','E90','E81','E132','E157','E148',
                                 'E137','E125','E149','E116']) #Setting channels for 
                                           #evoked response of Visual trigger
evoked_vis_r = epochs['vis_r'].average()
evoked_vis_r.plot(titles='Visual (flashing right) feedback evoked response', spatial_colors=True, gfp=True) #Plotting evoked response
                                                                                       # of visual channels


# In[19]:

evoked_vis_r.plot_topomap(times=np.arange(-0.1, 0.4, 0.05))
ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)

evoked_vis_r.plot_joint(title='Visual (flashing right) evoked response', times = [.0, 0.075, 0.125, 0.25],
                      ts_args=ts_args, topomap_args=topomap_args)


# In[30]:

left, right = epochs_vis_l["vis_l"].average(), epochs_vis_r["vis_r"].average()

# create and plot difference ERP
mne.combine_evoked([left, -right], weights='equal').plot_joint(times=np.arange(-0.2,0.5,0.15))


# ### "Letter"  inhibition trigger

# In[20]:

tmin = -0.5  # start of each epoch (200ms before the trigger)
tmax = 1  # end of each epoch (1000ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
epochs_lett = epochs.pick_channels(['E31','E32','E26','E25','E18','E19','E20','E27'
                                  'E33','E37','E9','E8','E24',
                                'E43','E52','E53','E80','E90','E81','E132','E157','E148',
                                  'E137','E125','E149','E116','E45','E186','E17'])
evoked_lett = epochs_lett['lett'].average()
evoked_lett.plot(titles='Button go/nogo evoked response', spatial_colors=True, gfp=True)


# In[34]:

mne.write_evokeds(evoked=evoked_lett,fname='loc_out_noepi_lett-ave.fif')


# In[21]:

evoked_lett.plot_joint(title='Button go/nogo evoked response', times = np.arange(-0.4, 1, 0.2),
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Auditory/Left

# In[22]:

tmin = -0.02  # start of each epoch (20ms before the trigger)
tmax = 0.075 # end of each epoch (75ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=baseline, preload=True, reject=reject)
epochs_aud_l = epochs.pick_channels(['E43','E52','E53','E80','E90','E81','E251'
                                     'E255','E73','E92','E91','E254','E250','E67',
                                    'E68','E69','E74','E227','E218',
                                     'E216','E233','E209','E232','E219'])
evoked_aud_l = epochs_aud_l['aud_l'].average()
evoked_aud_l.plot(titles='Auditory/Left evoked response', spatial_colors=True, gfp=True)


# In[23]:

mne.write_evokeds(evoked=evoked_aud_l, fname='loc_out_noepi_aud_l-ave.fif')


# In[24]:

evoked_aud_l.plot_joint(title='Auditory/Left evoked response', times = np.arange(-0.02, 0.075, 0.02),
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Auditory/Right

# In[25]:

tmin = -0.02  # start of each epoch (20ms before the trigger)
tmax = 0.075  # end of each epoch (75ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=baseline, preload=True, reject=reject) #need to redefine epochs each time
                                                                    #perhaps could be streamlined?
epochs_aud_r = epochs.pick_channels(['E43','E52','E53','E80','E90','E81','E251'
                                     'E255','E73','E92','E91','E254','E250','E67',
                                    'E68','E69','E74','E227','E218',
                                     'E216','E233','E209','E232','E219'])
evoked_aud_r = epochs_aud_r['aud_r'].average()
evoked_aud_r.plot(titles='Auditory/Right evoked response', spatial_colors=True, gfp=True)


# In[26]:

mne.write_evokeds(evoked=evoked_aud_r, fname='loc_out_noepi_aud_r-ave.fif')


# In[27]:

evoked_aud_r.plot_joint(title='Auditory/Right evoked response', times = np.arange(-.02, 0.075, 0.02),
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Average of Auditory trials

# In[28]:

left, right = epochs_aud_l["aud_l"].average(), epochs_aud_r["aud_r"].average()

# create and plot difference ERP
mne.combine_evoked([left, -right], weights='equal').plot_joint(times=np.arange(-0.02,0.075,0.015))

