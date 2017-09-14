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