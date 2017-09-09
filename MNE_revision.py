
# coding: utf-8

# #### --coding: utf-8--

# ## Import the data

# In[1]:

import Tkinter
import tkFileDialog
root = Tkinter.Tk()
filename = tkFileDialog.askopenfilename(parent=root, initialdir='/users/nikitaskoussis/Dropbox/Science/PVB304/Article/MNE', 
                                    title='Please select your EEG file')
root.destroy()


# ## Import the relevant libraries

# In[5]:

import mne
import scipy
import numpy 
import matplotlib
matplotlib.use('Qt5Agg')


# ## Read the raw file

# In[112]:

raw = mne.io.read_raw_eeglab(filename)
print(raw)
print(raw.info)


# In[5]:

print(raw.ch_names)


# ### Preprocessing for speed (may not be needed)

# In[78]:

#tmin, tmax = 20, 200
#raw.crop(tmin, tmax).load_data()  # 20s to 200s data segment for speed
#raw.plot(show_options=True) #plot of raw data


# ### Designating bad channels

# In[113]:

# bad channels
raw.info['bads'] = ['REF','E82','E102','E103','E111','E112','E113','E120','E121',
                    'E122','E123','E124','E133','E134','E135','E136','E145','E146',
                    'E147','E156','E167','E210','E229','E237','E256']
picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False,
                       exclude='bads')


# In[143]:

raw.plot_sensors() #plotting the sensor map in 2d
raw.plot_sensors(kind='3d', ch_type='eeg', ch_groups='position') #sensor map in 3d


# ### Projection mapping

# In[114]:

mne.set_eeg_reference(raw) #prevent MNE from setting reference automatically


# ### Power plot

# In[81]:

raw.plot_psd(average=False)


# ### Filtering of data

# In[116]:

raw.filter(l_freq=None, h_freq=50) #low-pass filter at 50 Hz
raw.filter(l_freq=1, h_freq=None) #high-pass filter at 1 Hz
raw.notch_filter(freqs=[50,100], picks=picks, filter_length='auto', phase='zero')


# In[84]:

raw.plot_psd(average=False)
raw.plot()


# ### Finding events

# In[136]:

events = mne.find_events(raw, stim_channel='STI 014', shortest_event=1)
event_id = {'lett' : 110, 'aud_l' : 137, 'aud_r' : 138, 'go/nogo' : 131, 'vis' : 88}
print(event_id)


# ### Event visualisation

# In[122]:

# Plot the events to get an idea of the paradigm
# Specify colors
color = {131: 'green', 138: 'yellow', 137: 'red', 110: 'black', 88: 'c'}

mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp, color=color,
                    event_id=event_id)


# ### Setting baseline

# In[123]:

baseline = (None, 0)  # means from the first instant to t = 0


# ### Peak-to-peak rejection parameters

# In[124]:

reject = dict(eeg=200e-6)


# ### Defining epochs and evoked responses for each trigger

# ### Visual trigger

# In[125]:

# event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                  baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
epochs_vis = epochs.pick_channels(['E9','E45','E186','E8','E17','E24',
                                  'E43','E52','E53','E80','E90','E81','E132','E157','E148',
                                'E137','E125','E149','E116']) #Setting channels for 
                                          #evoked response of Visual trigger
evoked_vis = epochs_vis['vis'].average()
evoked_vis.plot(titles='Visual feedback evoked response', spatial_colors=True, gfp=True) #Plotting evoked response
                                                                                      # of visual channels
evoked_vis.plot_topomap()


# #### More visualisation

# In[126]:

ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)

evoked_vis.plot_joint(title='Visual evoked response', times = [.0, 0.075, 0.125, 0.25],
                      ts_args=ts_args, topomap_args=topomap_args)


# ### "Letter"  trigger

# In[142]:

tmin = -0.5  # start of each epoch (200ms before the trigger)
tmax = 1  # end of each epoch (1000ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
epochs_lett = epochs.pick_channels(['E9','E45','E186','E8','E17','E24',
                                    'E43','E52','E53','E80','E90','E81','E132','E157','E148',
                                  'E137','E125','E149','E116'])
evoked_lett = epochs_lett['lett'].average()
evoked_lett.plot(titles='Button evoked response', spatial_colors=True, gfp=True)
evoked_lett.plot_topomap(title='Button evoked response power map over time')


# In[141]:

evoked_lett.plot_joint(title='Button evoked response', times = [0, 0.5, 1],
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Auditory/Left

# In[152]:

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
evoked_aud_l.plot_topomap()


# In[138]:

evoked_aud_l.plot_joint(title='Auditory/Left evoked response', times = [0, 0.018, 0.033],
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Auditory/Right

# In[153]:

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
evoked_aud_r.plot_topomap()


# In[140]:

evoked_aud_r.plot_joint(title='Auditory/Right evoked response', times = [0, 0.018, 0.033],
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Average of Auditory trials

# In[154]:

left, right = epochs_aud_l["aud_l"].average(), epochs_aud_r["aud_r"].average()

# create and plot difference ERP
mne.combine_evoked([left, -right], weights='equal').plot_joint(times=[0,0.018,0.025,0.033])


# ### Go/nogo inhibition task

# In[148]:

tmin = -0.5  # start of each epoch (200ms before the trigger)
tmax = 1  # end of each epoch (1000ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
epochs_go = epochs.pick_channels(['E31','E32','E26','E25','E18','E19','E20','E27'
                                  'E33','E37','E9','E45','E186','E8','E17','E24',
                                'E43','E52','E53','E80','E90','E81','E132','E157','E148',
                                  'E137','E125','E149','E116'])
evoked_go = epochs_go['go/nogo'].average()
evoked_go.plot(titles='Go/nogo task evoked response', spatial_colors=True, gfp=True)
evoked_go.plot_topomap(title='Go/nogo task evoked response power map over time')

