
# coding: utf-8

# In[1]:

#load in file for analysis
import Tkinter
import tkFileDialog
root = Tkinter.Tk()
fname = tkFileDialog.askopenfilename(parent=root, initialdir='/users/nikitaskoussis/Dropbox/Science/PVB304/Article/MNE',
                                    title='Please select your raw EEG file')
root.destroy()


# In[11]:

import mne
import scipy
import numpy as np
import matplotlib.pyplot as plt


# In[39]:

iter_freqs = [('Visual', 8, 13),
              ('Auditory', 40, 55)]


# In[40]:

frequency_map = list()


# In[41]:

event_id = dict(vis_l=87, aud_l=137, aud_r=138, vis_r=88)
tmin,tmax = -0.5, 1
baseline = (None, 0)

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


# In[42]:

# now we define the global field power

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


# In[44]:

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
    ax.set_xlim(-500, 1000)

axes.ravel()[-1].set_xlabel('Time [ms]')
fig.suptitle('Global Field Power over time')
plt.show()


# In[ ]:



