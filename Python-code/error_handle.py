
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
