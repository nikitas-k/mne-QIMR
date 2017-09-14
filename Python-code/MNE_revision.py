#### Function space

def ica_correction(raw, picks):
    
    # ## Function "ica_correction" will correct artifacts in eeg data
    # (eg. blink) using ICA and return an ICA array under "my-ica.fif"
    ## Will also plot ICA components
    
    from mne.preprocessing import ICA
    from mne.preprocessing import create_eog_epochs
    
    #ICA parameters
    n_components = 25  # if float, select n_components by explained variance of PCA
    method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
    decim = 3  # we need sufficient statistics, not all time points -> saves time
    
    # we will also set state of the random number generator - ICA is a
    # non-deterministic algorithm, but we want to have the same decomposition
    # and the same order of components each time this tutorial is run
    random_state = 23
        
    ica = ICA(n_components=n_components, method=method, 
                  random_state=random_state)
    ica.fit(raw, picks=picks, decim=decim, reject=dict(eeg=200e-6))
        
    ica.plot_components()
        
    eog_average = create_eog_epochs(raw, reject=dict(eeg=200e-6),
                                        picks=picks).average()
            
    n_max_eog = 1  # here we bet on finding the vertical EOG components
    eog_epochs = create_eog_epochs(raw, reject=dict(eeg=200e-6), picks=picks)  # get single EOG trials
    eog_inds, scores = ica.find_bads_eog(eog_epochs)  # find via correlation
            
    ica.plot_scores(scores, exclude=eog_inds)  # look at r scores of components
    # we can see that only one component is highly correlated and that this
    # component got detected by our correlation analysis (red).
            
    ica.plot_sources(eog_average, exclude=eog_inds)  # look at source time course
            
    ica.plot_properties(eog_epochs, picks=eog_inds, psd_args={'fmax': 35.},
                                image_args={'sigma': 1.})
                
    print(ica.labels_)
                                
    ica.plot_overlay(eog_average, exclude=eog_inds, show=False)
                                
    ica.exclude.extend(eog_inds)
    # from now on the ICA will reject this component even if no exclude
            # parameter is passed, and this information will be stored to disk
            # on saving
                                
            # uncomment this for reading and writing
    #ica.save('my-ica.fif')
    #ica = read_ica('my-ica.fif')
    
    
# coding: utf-8

def error_handle(epochs):
    
    #### Use this function to compute the errors involved in the experiment process. This function will output
    #### the noise covariance of the file as a figure.

    ## Computing noise covariance
    noise_cov = mne.compute_covariance(epochs, tmax=0., method=['shrunk', 'empirical'])
    
    fig_cov, fig_spectra = mne.viz.plot_cov(noise_cov, raw.info)
    
    ## Compute evoked response
    evoked = epochs.average()
    evoked.plot()
    evoked.plot_topomap(times=np.linspace(0.05, 0.15, 5), ch_type='eeg')
        
        # Show whitening
    evoked.plot_white(noise_cov)
    
def time_frequency_analysis(raw, events, event_id, tmin, tmax, baseline, reject):

    #### This function will do time-frequency analysis for you and
    #### return a plot of Global Field Power with confidence intervals.

    iter_freqs = []

    for x in range(event_id[0], len(event_id)):
    
        s = input('Enter your minimum and maximum frequency for event %event_id[x] ')
        if len(s) != 2:
            return('Please input only two (2) frequencies')  #end in error
        elif s != float:
            return('Please input only numbers')
        elif s == []:
            return('Field was empty, please enter values')
        elif s[1] > s[2]:
            return('Please make sure your frequencies are min to max')
        else:
            s = s[1:len(s)-1]
            t = s.split(",")
            freq_range = []
            for case_t in t:
                freq_range.append(int(case_t))

    iter_freqs = '' + [(event_id[x], freq_range)]






    frequency_map = list()

    #get the header to extract events
    raw = mne.io.read_raw_eeglab(fname, preload=False)
    events = mne.find_events(raw, shortest_event=0, stim_channel='STI 014')

    for band, fmin, fmax in iter_freqs:
        # (re)load the data to save memory
        raw = mne.io.read_raw_eeglab(fname, preload=True)
        raw.info['bads'] = ['REF','E82','E102','E103','E111','E112','E113','E120','E121',
                            'E122','E123','E124','E133','E134','E135','E136','E145','E146',
                            'E147','E156','E167','E210','E229','E237','E256']
        raw.pick_types(eeg=True, exclude='bads')  # we just look at EEGs
                
        # bandpass filter and compute Hilbert
        raw.filter(fmin, fmax, n_jobs=1,  # use more jobs to speed up.
                           l_trans_bandwidth=1,  # make sure filter params are the same
                           h_trans_bandwidth=1,  # in each band and skip "auto" option.
                           )
        raw.apply_hilbert(n_jobs=1, envelope=False)
                        
        epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline=baseline,
                                            reject = dict(eeg=200e-6), preload=True)
                            # remove evoked response and get analytic signal (envelope)
        epochs.subtract_evoked()  # for this we need to construct new epochs.
        epochs = mne.EpochsArray(
                                                     data=np.abs(epochs.get_data()), info=epochs.info, tmin=epochs.tmin)
                            # now average and move on
        frequency_map.append(((band, fmin, fmax), epochs.average()))

    rng = np.random.RandomState(42)


    def get_gfp_ci(average, n_bootstraps=2000):
        """get confidence intervals from non-parametric bootstrap"""
        indices = np.arange(len(average.ch_names), dtype=int)
        gfps_bs = np.empty((n_bootstraps, len(average.times)))
        for iteration in range(n_bootstraps):
            bs_indices = rng.choice(indices, replace=True, size=len(indices))
            gfps_bs[iteration] = np.sum(average.data[bs_indices] ** 2, 0)
        gfps_bs = mne.baseline.rescale(gfps_bs, average.times, baseline=(None, 0))
        ci_low, ci_up = np.percentile(gfps_bs, (2.5, 97.5), axis=0)
        return ci_low, ci_up

    # now we can track the emergence of spatial patterns in the frequency band

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, sharey=True)
    colors = plt.cm.viridis((0.1, 0.35, 0.75, 0.95))
    for ((freq_name, fmin, fmax), average), color, ax in zip(
                                                             frequency_map, colors, axes.ravel()[::-1]):
        times = average.times * 1e3
        gfp = np.sum(average.data ** 2, axis=0)
        gfp = mne.baseline.rescale(gfp, times, baseline=(None, 0))
        ax.plot(times, gfp, label=freq_name, color=color, linewidth=2.5)
        ax.plot(times, np.zeros_like(times), linestyle='--', color='red',
                linewidth=1)
        ci_low, ci_up = get_gfp_ci(average)
        ax.fill_between(times, gfp + ci_up, gfp - ci_low, color=color,
                                alpha=0.3)
        ax.grid(True)
        ax.set_ylabel('GFP')
        ax.annotate('%s (%d-%dHz)' % (freq_name, fmin, fmax),
                                        xy=(0.95, 0.8),
                                        horizontalalignment='right',
                                        xycoords='axes fraction')
        ax.set_xlim(-tmin*1000, tmax*1000)

    axes.ravel()[-1].set_xlabel('Time [ms]')
    fig.suptitle('Global Field Power over time')
    plt.show()


# #### --coding: utf-8--

# ## Import the data

import Tkinter
import tkFileDialog
root = Tkinter.Tk()
fname = tkFileDialog.askopenfilename(parent=root, initialdir='/',
                                    title='Please select your EEG file')
root.destroy()


# ## Import the relevant libraries

import mne
import scipy
import numpy as np
import matplotlib.pyplot as plt


# ## Read the raw file

raw = mne.io.read_raw_eeglab(fname) #see http://martinos.org/mne/stable/python_reference.html#reading-raw-data for more info on how to read eeg data into the program
print(raw)
print(raw.info)
print(raw.ch_names)

# ### Preprocessing for speed (may not be needed)

# tmin, tmax = 20, 200
# raw.crop(tmin, tmax).load_data()  # 20s to 200s data segment for speed
# raw.plot(show_options=True) #plot of raw data
# uncomment if you wish to trim the data

# ### Designating bad channels

# bad channels
raw.info['bads'] = ['REF','E82','E102','E103','E111','E112','E113','E120','E121',
                            'E122','E123','E124','E133','E134','E135','E136','E145','E146',
                            'E147','E156','E167','E210','E229','E237','E256'] #input your own bad channels here
picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False,
                       exclude='bads') # setting for eeg data, will have to change values to other
#                                       values for any other types of data to True.

# ### Sensor mapping

raw.plot_sensors() #plotting the sensor map in 2d
raw.plot_sensors(kind='3d', ch_type='eeg', ch_groups='position') #sensor map in 3d


# ### Projection mapping

mne.set_eeg_reference(raw) #prevent MNE from setting reference automatically


# ### Power plot

raw.plot_psd(average=False)


# ### Filtering of data

raw.filter(l_freq=None, h_freq=55) #low-pass filter at 55 Hz (set your own frequencies here if you prefer something else)
raw.filter(l_freq=1, h_freq=None) #high-pass filter at 1 Hz
raw.notch_filter(freqs=[50,100], picks=picks, filter_length='auto', phase='zero') # run cell twice

# plot the power spectral density and the raw data to see what it looks like now
raw.plot_psd(average=False)
raw.plot()

# ### Finding events

events = mne.find_events(raw, stim_channel='STI 014', shortest_event=1)
event_id = {'lett' : 110, 'aud_l' : 137, 'aud_r' : 138, 'vis_l' : 87, 'vis_r' : 88} #define your own events here
mne.write_events(event_list=events, filename='%fname-eve.fif')


# ### Event visualisation

# Plot the events to get an idea of the paradigm
# Specify colors
color = {87: 'green', 138: 'yellow', 137: 'red', 110: 'black', 88: 'c'}

mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp, color=color,
                    event_id=event_id)


# ### Setting epoch parameters

baseline = (None, 0)  # means from the first instant to t = 0
reject = dict(eeg=200e-6) # reject any environmental interference from the epoch


## ICA correction

ica_correction(raw, picks)

# ### Defining epochs and evoked responses for each trigger

# ### Visual trigger

# event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                  baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
#epochs_vis_l = epochs.pick_channels() #Setting channels for
                                          #evoked response of Visual trigger
evoked_vis_l = epochs['vis_l'].average()
evoked_vis_l.plot(titles='Visual (flashing left) feedback evoked response', spatial_colors=True, gfp=True) 
#Plotting evoked response of visual channels

mne.write_evokeds(evoked=evoked_vis_l,fname='%fname_vis_l-ave.fif')


# #### More visualisation

evoked_vis_l.plot_topomap(times=np.arange(-0.1, 0.4, 0.05))
ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)

evoked_vis_l.plot_joint(title='Visual (flashing left) evoked response', times = [.0, 0.075, 0.125, 0.25],
                      ts_args=ts_args, topomap_args=topomap_args)

# event trigger and conditions
tmin = -0.2  # start of each epoch (200ms before the trigger)
tmax = 0.5  # end of each epoch (500ms after the trigger)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                   baseline=baseline, preload=True, reject=reject)
epochs.drop_bad()
    #epochs_vis_r = epochs.pick_channels() #Setting channels for
                                           #evoked response of Visual trigger
evoked_vis_r = epochs['vis_r'].average()
evoked_vis_r.plot(titles='Visual (flashing right) feedback evoked response', spatial_colors=True, gfp=True) #Plotting evoked response
    # of visual channels

mne.write_evokeds(evoked=evoked_vis_r,fname= '%fname_vis_r-ave.fif')


# more visualisation

evoked_vis_r.plot_topomap(times=np.arange(-0.1, 0.4, 0.05))
ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)

evoked_vis_r.plot_joint(title='Visual (flashing right) evoked response', times = [.0, 0.075, 0.125, 0.25],
                      ts_args=ts_args, topomap_args=topomap_args)

left, right = epochs["vis_l"].average(), epochs["vis_r"].average()

# create and plot difference ERP
mne.combine_evoked([left, -right], weights='equal').plot_joint(times=np.arange(-0.2,0.5,0.15))


# ### "Letter"  inhibition trigger

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

mne.write_evokeds(evoked=evoked_lett,fname= '%fname_lett-ave.fif')

evoked_lett.plot_joint(title='Button go/nogo evoked response', times = np.arange(-0.4, 1, 0.2),
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Auditory/Left

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

mne.write_evokeds(evoked=evoked_aud_l, fname='%fname_aud_l-ave.fif')

evoked_aud_l.plot_joint(title='Auditory/Left evoked response', times = np.arange(-0.02, 0.075, 0.02),
                      ts_args=ts_args, topomap_args=topomap_args)


# ### Auditory/Right

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

mne.write_evokeds(evoked=evoked_aud_r, fname='%fname_aud_r-ave.fif')

evoked_aud_r.plot_joint(title='Auditory/Right evoked response', times = np.arange(-.02, 0.075, 0.02),
                      ts_args=ts_args, topomap_args=topomap_args)

mne.write_evokeds(evoked=evoked_aud_r, fname='%fname_aud_r-ave.fif')

# ### Average of Auditory trials

left, right = epochs_aud_l["aud_l"].average(), epochs_aud_r["aud_r"].average()

# create and plot difference ERP
mne.combine_evoked([left, -right], weights='equal').plot_joint(times=np.arange(-0.02,0.075,0.015))
