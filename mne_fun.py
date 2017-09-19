#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import mne
import scipy
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_topo_compare():
    
    """This function will compare evoked potentials across conditions
    given one channel to look at"""
    
    
    import matplotlib.pyplot as plt
    from mne.viz import plot_evoked_topo
    
    include = [raw_input('Please select the channel you wish to look at: ')]
    reject = dict(eeg=200e-6)
    picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=True,
                           include=include, exclude='bads')
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax,
                picks=picks, baseline=(None, 0), reject=reject)
    
    # Generate list of evoked objects from conditions names
    evokeds = [epochs[name].average() for name in event_id]
    
    colors = 'yellow', 'green'
    
    key, value = event_id
    title = ("Topographical map of evoked response comparing \n%s to %s as conditions" % key, value)

    plot_evoked_topo(evokeds, color=colors, 
                     title=title)

    plt.show()

def sensor_least_squares(epochs):
    
    """This function will process the sensor least squares regression,
    outputting a regression coefficient that will denote the efficiency
    of each combination of sensor and timepoint. P-values and T statistics
    are also computed."""
        
    from mne.stats.regression import linear_regression
        
    names = ['intercept', 'trial-count']
        
    intercept = np.ones((len(epochs),), dtype=np.float)
    design_matrix = np.column_stack([intercept,  # intercept
                             np.linspace(0, 1, len(intercept))])

    # also accepts source estimates
    lm = linear_regression(epochs, design_matrix, names)


    def plot_topomap(x, unit):
        x.plot_topomap(ch_type='eeg', scale=1, size=1.5, vmax=np.max,
                       unit=unit, times=np.linspace(0.1, 0.2, 5))

    trial_count = lm['trial-count']

    plot_topomap(trial_count.beta, unit='z (beta)')
    plot_topomap(trial_count.t_val, unit='t')
    plot_topomap(trial_count.mlog10_p_val, unit='-log10 p')
    plot_topomap(trial_count.stderr, unit='z (error)')

def erp_regression(raw, events, event_id, tmin, tmax, reject, baseline):
    
    """This function processes the linear least-squares fitting of the 
    event-related potential of raw data
    Estimation of ERP compared to actual ERP"""

    from mne.stats.regression import linear_regression_raw
    # standard epoching
    epochs = mne.Epochs(raw, events, event_id,
                        tmin, tmax, reject = None,
                        baseline = None, preload=True)
    
    epochs.resample(150, npad='auto', n_jobs=1)

    evokeds = linear_regression_raw(raw, events=events, event_id=event_id, reject = None, tmin=tmin, tmax=tmax)
     # linear_regression_raw returns a dict of evokeds
     # select a condition similar to mne.Epochs objects

    cond = raw_input("Please input the event ID you wish to plot the regression for: ")
    if cond in event_id == True:
        fig, (ax1, ax2, ax3) = fig.subplots(3, 1)
        params = dict(spatial_colors=True, show=False, ylim=dict(eeg=(-10, 10)))
        epochs[cond].average().plot(axes=ax1, **params)
        evokeds[cond].plot(axes=ax2, **params)
        contrast = mne.combine_evoked([evokeds[cond], -epochs[cond].average()],
                                       weights='equal')
        contrast.plot(axes=ax3, **params)
        ax1.set_title("Traditional averaging")
        ax2.set_title("rERF")
        ax3.set_title("Difference")
        plt.show()

def ica_correction(raw, picks):
        
    """Function "ica_correction" will correct artifacts in eeg data
    (eg. blink) using ICA and return an ICA array under "my-ica.fif"
    Will also plot ICA components"""
    
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
    
    n_max_eog = 1 #don't expect to find horizontal eog components
    title = 'Sources related to EOG components (red)'

    eog_epochs = create_eog_epochs(raw, tmin=-.5, tmax=1, picks=picks)
    eog_inds, scores = ica.find_bads_eog(eog_epochs)
    ica.plot_scores(scores, exclude=eog_inds, 
                    title=title, 
                    labels='eog')
    
    show_picks = np.abs(scores).argsort()[::-1][:5]
        
    ica.plot_sources(raw, show_picks, exclude=eog_inds, title=title)
    ica.plot_components(eog_inds, title=title, colorbar=True)
    
    eog_inds = eog_inds[:n_max_eog]
    ica.exclude += eog_inds

    # uncomment this for reading and writing
    #ica.save('my-ica.fif')
    #ica = read_ica('my-ica.fif')
    #apply to epochs
    ica.apply(epochs)
    
def error_handle(epochs):
    
    """Use this function to compute the errors involved in the experiment 
    process. This function will output
    the noise covariance of the file as a figure.
    NOTE: This function hogs CPU and takes a long time. Only use this
    if you really need to."""
    print('This function will take a long time. Please be patient.')
    ## Computing noise covariance
    epochs.resample(150, npad='auto', n_jobs=1)
    noise_cov = mne.compute_covariance(epochs, tmax=0., method=['shrunk', 'empirical'])
    
    fig_cov, fig_spectra = mne.viz.plot_cov(noise_cov, raw.info)
    
    ## Compute evoked response
    epochs.resample(150, npad='auto', n_jobs=1)
    evoked = epochs.average()
    evoked.plot()
    evoked.plot_topomap(times=np.linspace(0.05, 0.15, 5), ch_type='eeg')
        
    # Show whitening
    evoked.plot_white(noise_cov)
    
def time_frequency_analysis_gfp(fname, montage, events, event_id, 
                                    picks, tmin, tmax, reject):

    """This function will do time-frequency analysis for you and
    return a plot of Global Field Power with confidence intervals."""
    
    iter_freqs = []
        
    for key, value in event_id.iteritems():
            
        s = int(input("Enter your minimum for '{evt}' ".format(evt=event_id[key])))
        t = int(input("Enter your maximum for '{evt}' ".format(evt=event_id[key])))
        if int(s) >= int(t):
            raise ValueError('Unexpected order')
        else:
            iter_freqs.append([str(event_id[key]), s, t])
    
    print('This function takes a long time to process if your file is very large (>200 MB)')
    print('You may wish to trim your data for speed. Please be patient...')
    
    frequency_map = list()
    
    for band, fmin, fmax in iter_freqs:
        # (re)load the data to save memory
        raw = mne.io.read_raw_brainvision(fname, montage, preload=True, eog=['EOG'])
        picks=picks  # we just look at EEGs
                
        # bandpass filter and compute Hilbert
        raw.filter(fmin, fmax, n_jobs=1,  # use more jobs to speed up.
                   l_trans_bandwidth=1,  # make sure filter params are the same
                   h_trans_bandwidth=1,  # in each band and skip "auto" option.
                   )
        raw.apply_hilbert(n_jobs=1, envelope=False)
                        
        epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline= (None, 0),
                            reject = dict(eeg=200e-6), preload=True)
        epochs.resample(150, npad='auto', n_jobs=1)
        # remove evoked response and get analytic signal (envelope)
        epochs.subtract_evoked()  # for this we need to construct new epochs.
        epochs = mne.EpochsArray(data=np.abs(epochs.get_data()), 
                                 info=epochs.info, tmin=epochs.tmin)
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
    for ((freq_name, fmin, fmax), average), color, ax in zip(frequency_map, colors, axes.ravel()[::-1]):
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
        ax.set_xlim(tmin*1000, tmax*1000)

    axes.ravel()[-1].set_xlabel('Time [ms]')
    fig.suptitle('Global Field Power over time')
    plt.show()
    
    
def time_frequency_analysis(fname, montage, events, event_id, 
                                picks, tmin, tmax, reject):
        
    """This function will do time-frequency analysis for you and
    return a plot of Global Field Power with confidence intervals."""
    
    iter_freqs = [('slow-vis', 5, 9,),
                      ('fast-vis', 10, 16)]
        
    print('This function takes a long time to process if your file is very large (>200 MB)')
    print('You may wish to trim your data for speed. Please be patient...')
        
    frequency_map = list()
        
    for band, fmin, fmax in iter_freqs:
        # (re)load the data to save memory
        raw = mne.io.read_raw_brainvision(fname, montage, preload=True, eog=['EOG'])
        picks=picks  # we just look at EEGs
                    
        # bandpass filter and compute Hilbert
        if fmin > 1:
            raw.filter(fmin, fmax, n_jobs=1,  # use more jobs to speed up.
                       l_trans_bandwidth=1,  # make sure filter params are the same
                       h_trans_bandwidth=1,  # in each band and skip "auto" option.
                       )
            raw.apply_hilbert(n_jobs=1, envelope=False)
            
            epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline= (None, 0),
                                reject = dict(eeg=200e-6), preload=True)
            # remove evoked response and get analytic signal (envelope)
            epochs.resample(150, npad='auto', n_jobs=1)
            epochs.subtract_evoked()  # for this we need to construct new epochs.
            epochs = mne.EpochsArray(data=np.abs(epochs.get_data()), 
                                     info=epochs.info, tmin=epochs.tmin)
            # now average and move on
            frequency_map.append(((band, fmin, fmax), epochs.average()))
        else:
            raw.filter(l_freq=None, h_freq=fmax, n_jobs=1)
            raw.apply_hilbert(n_jobs=1, envelope=False)
            epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline= (None, 0),
                                reject = dict(eeg=200e-6), preload=True)
            # remove evoked response and get analytic signal (envelope)
            epochs.resample(150, npad='auto', n_jobs=1)
            epochs.subtract_evoked()  # for this we need to construct new epochs.
            epochs = mne.EpochsArray(data=np.abs(epochs.get_data()), 
                                     info=epochs.info, tmin=epochs.tmin)
            # now average and move on
            frequency_map.append(((band, fmin, fmax), epochs.average()))
        
    rng = np.random.RandomState(42)


    def get_voltage_ci(average, n_bootstraps=2000):
        """get confidence intervals from non-parametric bootstrap"""
        indices = np.arange(len(average.ch_names), dtype=int)
        v_bs = np.empty((n_bootstraps, len(average.times)))
        for iteration in range(n_bootstraps):
            bs_indices = rng.choice(indices, replace=True, size=len(indices))
            v_bs[iteration] = np.sum(average.data[bs_indices] ** 2, 0)
            v_bs = mne.baseline.rescale(v_bs, average.times, baseline=(None, 0))
            ci_low, ci_up = np.percentile(v_bs, (2.5, 97.5), axis=0)
        return ci_low, ci_up
        # now we can track the emergence of spatial patterns in the frequency band

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, sharey=True)
    colors = plt.cm.viridis((0.1, 0.35, 0.75, 0.95))
    for ((freq_name, fmin, fmax), average), color, ax in zip(
            frequency_map, colors, axes.ravel()[::-1]):
        times = average.times * 1e3
        v = np.sum(average.data, axis=0) * 1e3 #correction for microvolts
        v = mne.baseline.rescale(v, times, baseline=(None, 0))
        ax.plot(times, v, label=freq_name, color=color, linewidth=2.5)
        ax.plot(times, np.zeros_like(times), linestyle='--', color='red',
                linewidth=1)
        ci_low, ci_up = get_voltage_ci(average)
        ax.fill_between(times, v + ci_up, v - ci_low, color=color,
                        alpha=0.3)
        ax.grid(True)
        ax.set_ylabel('uV')
        ax.annotate('%s (%d-%dHz)' % (freq_name, fmin, fmax),
                    xy=(0.95, 0.8),
                    horizontalalignment='right',
                    xycoords='axes fraction')
        ax.set_xlim(tmin*1000, tmax*1000)

    axes.ravel()[-1].set_xlabel('Time [ms]')
    fig.suptitle('Evoked response to stimulus at specific frequencies')
    plt.show()
    
    
def concatenate_evokeds(path):
    """This function will concatenate the evoked files of individual subjects
    so that it can be passed to processing or plotting"""
    
    subs_epo = []
    vis_all = []
    lett_all = []
    
    for filename in os.listdir(path):
        if filename.endswith("-ave.fif"):
            subs_epo = mne.read_evokeds(filename)
        else:
            ValueError('No evoked files detected.')
        
        vis_all = vis_all + mne.epochs.concatenate_epochs([subs_epo['vis']])
        lett_all = lett_all + mne.epochs.concatenate_epochs([subs_epo['lett']])
            