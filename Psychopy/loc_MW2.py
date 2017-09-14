#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.2),
    on September 04, 2017, at 11:16
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
from psychopy import prefs
prefs.general['audioLib'] = ['pysoundcard']

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'loc_v1'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1280, 1024), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "do_video"
do_videoClock = core.Clock()
import time
import threading
import copy



# initiate my visual stimuli:
vis_times={'8':[0.001,0.111, 0.253,0.373,0.475, 0.600],'13':[0.001,0.078,0.151,0.214,0.300,0.376,0.442,0.525,0.600]}


class play_vis_stim(threading.Thread):
    def __init__(self,vis_times,side,freq):
        threading.Thread.__init__(self)
        self.win=win
        # is this it?
        self.hit_times=copy.deepcopy(vis_times[freq])
        self.side=side
        self.flash=0
        self.isstarted=0


    def run(self):

        print('started visual thread...')
        self.isstarted=1
        # get the list
        hit_times = self.hit_times
        # this is to make things run/work
        max_time = hit_times[-1]
        hit_times[-1] = -1

        start_time=time.time()
        target_time = hit_times.pop(0)

        while True:
            current_time = time.time() - start_time
            if current_time >target_time and target_time > 0:
    
                #print current_time
                #print target_time
                #print 'flashed'

                self.flash=1;

                # get us a NEW target time !!
                target_time = hit_times.pop(0)

            if current_time>max_time:
                #print 'broke while loop at time = %f ' % current_time
                break
    
            time.sleep(0.0005)

    def resetFlash(self):
        self.flash=0

    def queryFlash(self):
        return self.flash

    def getSide(self):
        return self.side

    def isStarted(self):
        return self.isstarted

# Initialize components for Routine "do_audio"
do_audioClock = core.Clock()
import threading
import time


# define my dict.
sounds={'left':{'40':sound.Sound('stim/audio_40Hz_L.wav', secs=-1),'55':sound.Sound('stim/audio_55Hz_L.wav', secs=-1)},'right':{'40':sound.Sound('stim/audio_40Hz_R.wav', secs=-1),'55':sound.Sound('stim/audio_55Hz_R.wav', secs=-1)}}

# initiate my volumes...
sounds['left']['40'].setVolume(1)
sounds['right']['40'].setVolume(1)
sounds['left']['55'].setVolume(1)
sounds['right']['55'].setVolume(1)


class play_audio_stim(threading.Thread):
    def __init__(self,sounds,side,freq):
        threading.Thread.__init__(self)
        self.side=side
        self.freq=freq
        self.sounds=sounds
        self.isstarted=0
    def run(self):
        print('started audio thread...')
        self.isstarted=1
        start_time=time.time()
        sounds=self.sounds
        freq=self.freq
        side=self.side

        # current_time = time.time() - start_time
        # print current_time
        my_sound = sounds[side][freq]
        my_sound.play()
        # ... aaand... we neatly wait untill the sound has been finished!
        time.sleep(my_sound.getDuration())
        current_time = time.time() - start_time
        print '---'
        print current_time

        
    def isStarted(self):
        return self.isstarted

# Initialize components for Routine "do_letters"
do_lettersClock = core.Clock()
text_stim = visual.TextStim(win=win, ori=0, name='text_4',
    text='X',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)


# quick and dirty shift function. Matlab has got its own built-in 'circshift' - I need to do it like this, now.
import random # if I didn't , already! - or if psychopy didn't , already.
def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

# doesn't matter if it's a set or if it's a list, for our purposes
# list comprehension uppercase trick:
letters_for_letter_stream = ['m','w','w','m']
letters_for_letter_stream = [x.upper() for x in letters_for_letter_stream]


# the letter_stream could be done better and made more general. Now it's too focussed on 'letters', but it should be really focussed on 'characters' or 'strings', or whatever kind of elements may be.
# the only thing is - in psychopy, it's not that easy to search-and-replace. In matlab it would've been quicker (for now). Program it in Spyder.. seems to be interesting!

class letter_stream(threading.Thread):
    def __init__(self,letters,switch_frequency,switch_probability):
        threading.Thread.__init__(self)

        self.letters=letters
        self.flag = 0
        self.switch_frequency=switch_frequency
        self.switch_probability = switch_probability
        self.isstarted=0
        self.current_letter='X'
        self.stop = 0
        self.pause=1


    def run(self):
        print('started letter thread...')
        self.isstarted=1
        start_time=time.time()

        letters=self.letters
        switch_frequency=self.switch_frequency
        switch_probability=self.switch_probability


        cal_time = time.time()
        # keep on doing this - until the end of the experiment, when I 'quit' the CORE:
        while True:

            # if the time bigger than the 'cal' time:
            if time.time() - cal_time > 0:
                # effecively, only run this code-block once every letter_time_interval:
                cal_time = cal_time + switch_frequency
                # switch the letter - according to the given chance:
                if random.random() < switch_probability:
                    letters = shift(letters,-1)
                else:
                    letters = shift(letters,1)
                # set the 'current' letter.
                self.current_letter = letters[0]
                # set the flag, too.
                self.flag = 1
            
                if self.pause==0:
                    self.current_letter = letters[0]
                    self.pause=1
                elif self.pause==1:
                    self.current_letter = (' ')
                    self.pause = 0 
            
            # sleep - for only a short time.
            time.sleep(0.01)
    
            if self.stop:
                break



    def getLetter(self):
        return self.current_letter

    def isStarted(self):
        return self.isstarted

    def queryFlag(self):
        if self.flag==1:
            self.flag = 0
            return 1
        else:
            return 0

    def setStop(self):
        self.stop=1


# Initialize components for Routine "do_triggers"
do_triggersClock = core.Clock()
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:57:03 2015

@author: Johan
"""
# this is all I need to make my experiment output some triggers.
# USAGE (very simple):

# check the sender objects - use the one appropriate!
# then - instantiate an ev_thread - give as agurment an instantiation of the appropriate sender object.

#   evt = evt_thread(egi_sender())

# then  start it:

#   evt.start()

# then - send events like so (i.e., strings!)
# brain products DOES wish only for INTs, though. That sort of sucks, given that EGI accepts strings. Naja. Implement it anyway.

#   evt.send(10)

# finally, at the end of the experiment  - stop it

#   evt.stop()


# a class that sends events regardless of attached device. So that during my experiment, I don't
# have to worry aobut that - the abstraction lies in here.

# written on-the-fly. So abstractions are right now something to improve upon.
# like: where do I do my device-specific stuff, do I make own functions for them, and where?
# right now I opted to have it distributed into the class itself, while in prinicple,
# it's nicer to maybe even make sub-classes per device for easy implementation later on.
# hmm - maybe I shoudl do this anyway. Damn.

# let's see how much the quick-n-dirty class implementation method of work would be
# improved by using python and NOT matlab - the king of quick n dirty.


# stuff we beed to send stuff:
import egi.simple as egi
# import parallel
import threading

import time

# fill in later to allow me to send BP triggers via parallel.
# most easy now - i just need to take care to instantiate the right object.
# and THEN - I just use init, send and finish!!
# maybe I could even make a super-class of this.
# but not.. now..
class brain_products_sender():
    def __init__(self):
        pass
    
    def init(self):
        pass
    
    def send(self,ev):
        pass
    
    def finish(self):
        pass
    

# this looks a little bit cleaner, already - i can focus just on one class if i wish
# to implement another recorder.
class egi_sender():
    def __init__(self):
        pass
        
    def init(self):
        ns = egi.Netstation()
        ns.connect('10.0.0.42', 55513) # sample address and port -- change according to your network settings            
        ns.BeginSession()     
        ns.sync()     
        ns.StartRecording()
        # save it to obj namespace for later use.
        self.ns=ns
        
    def send(self,ev):
        ns = self.ns
        timestamp = egi.ms_localtime()
        ns.send_event( ev, label=ev, timestamp=timestamp, table = {'label' : ev, 'timestamp' : timestamp} ) 
        
    def finish(self):
        ns = self.ns
        ns.StopRecording()
        ns.EndSession()
        ns.disconnect()


# the MAIN class: ev_sender!
class ev_thread(threading.Thread):
    
    # init asks you for what kind of device you have attached
    # it also inits for you - if needed
    def __init__(self,sender_obj):
        # overload..
        threading.Thread.__init(self)
        # output_device can be either:
        # 'no_device'
        # 'egi'
        # 'brain_products'
        # !!! instantiate THIS object with a sender object!
        self.sender = sender_obj
        self.ev_list=[]
        # for clean exit
        self.stop_sending = 0
        # do the init stuff separately (necessary) - makes you work for it
        self.sender.init()

        
    def run(self):

        # apply the LIFO rule for sending events.
        while len(self.ev_list)>0:

            # pop it..
            ev=self.ev_list.pop(0)

            # send it!
            self.sender.send(ev)
            
            # arrange for a clean exit
            if self.stop_thread == 1:
                # disconnect, etc etc:
                self.sender.stop()
                # then - exit this loop.
                break
            
            # make sure the processor doens't take it all up!
            # allow for 1 msec time inaccuracy, too.
            time.sleep(0.001)

    def send(self,ev):
        # just append it to the list - so it'll be taken off in the main while loop.
        self.ev.append(ev)
        
        
    def stop(self):
        self.stop_thread = 1
        
select_eeg_system = visual.TextStim(win=win, name='select_eeg_system',
    text="What is your EEG system?\n\n1) Nothing (don't send triggers)\n\n2) EGI\n\n3) Brain Products",
    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);


# Initialize components for Routine "instr"
instrClock = core.Clock()
instr_text = visual.TextStim(win=win, name='instr_text',
    text="Keep focusing on the centre of the screen\n\nThe letters M or W will appear\n\n-Press 'm' if you see the letter M\n-Press 'w' if you see the letter W\n\nRespond as quickly as possible\n\npress space bar to begin",
    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "main_routine"
main_routineClock = core.Clock()
# this code block has 2 functions - (1) control time flow of the experimen, and (2) control visual elements/flashes

import time
checkerboard_hidden=True
# for future reference: I need a struct (!) telling me what is 'inside' the visual stimulus - at all times!!

# generated with a matlab script, so we can play around with other timing options
# stuff that happens left is always equally long as stuff that happens right - good for fMRI
# difference between 2 frequencies I cannot make exactly the same - so anything that compares frequencies should have NORMALIZED power


only_audio = [[10.,20.,'audio',['left','40']],[112.5,130.,'audio',['left','40']],[242.5,260.,'audio',['left','40']],[50.,60.,'audio',['left','55']],[195.,205.,'audio',['left','55']],[312.5,330.,'audio',['left','55']],[30.,40.,'audio',['right','40']],[147.5,165.,'audio',['right','40']],[277.5,295.,'audio',['right','40']],[77.5,95.,'audio',['right','55']],[175.,185.,'audio',['right','55']],[215.,225.,'audio',['right','55']]]
only_video = [[17.5,35.,'video',['left','8']],[135.,145.,'video',['left','8']],[280.,290.,'video',['left','8']],[87.5,105.,'video',['left','13']],[217.5,235.,'video',['left','13']],[320.,330.,'video',['left','13']],[52.5,70.,'video',['right','8']],[155.,165.,'video',['right','8']],[300.,310.,'video',['right','8']],[115.,125.,'video',['right','13']],[182.5,200.,'video',['right','13']],[252.5,270.,'video',['right','13']]]

# this lasts for 5 minutes and 40 seconds in total (last 10 secs is REST)
all_stims = [[10.,20.,'audio',['left','40']],[112.5,130.,'audio',['left','40']],[242.5,260.,'audio',['left','40']],[50.,60.,'audio',['left','55']],[195.,205.,'audio',['left','55']],[312.5,330.,'audio',['left','55']],[30.,40.,'audio',['right','40']],[147.5,165.,'audio',['right','40']],[277.5,295.,'audio',['right','40']],[77.5,95.,'audio',['right','55']],[175.,185.,'audio',['right','55']],[215.,225.,'audio',['right','55']],[17.5,35.,'video',['left','8']],[135.,145.,'video',['left','8']],[280.,290.,'video',['left','8']],[87.5,105.,'video',['left','13']],[217.5,235.,'video',['left','13']],[320.,330.,'video',['left','13']],[52.5,70.,'video',['right','8']],[155.,165.,'video',['right','8']],[300.,310.,'video',['right','8']],[115.,125.,'video',['right','13']],[182.5,200.,'video',['right','13']],[252.5,270.,'video',['right','13']]]
all_timings = all_stims
max_time = 340.;


# right checkerboard stimuli
right_cb = visual.RadialStim(win, tex='sqrXsqr', color=1, size=2,
                             visibleWedge=[0., 181.], radialCycles=5,
                             angularCycles=10, interpolate=False, 
                             angularPhase=2*3.141592/360/20,autoLog=False)
# right_cb_fl=right_cb
# right_cb_fl.setAngularPhase(90)
  
# left checkerboard stimuli
left_cb = visual.RadialStim(win, tex='sqrXsqr', color=1, size=2,
                            visibleWedge=[179.99, 360.], radialCycles=5,
                            angularCycles=10, interpolate=False,
                            angularPhase=2*3.141592/360/20,autoLog=False)
# left_cb_fl=left_cb
# left_cb_fl.setAngularPhase(90)

  
# fixation dot
fixation = visual.PatchStim(win, color=-0.5, colorSpace='rgb', tex=None,
                            mask='circle', size=0.1)


vis_contents = [right_cb,left_cb,fixation,text_stim]


def doFlash(win,vis_contents,side):

    # extract again the visual contents:
    right_cb = vis_contents[0]
    left_cb=vis_contents[1]
    fixation=vis_contents[2]
    text_stim=vis_contents[3]

    if side=='left':
        left_cb.contrast = -1.*left_cb.contrast
    elif side=='right':
        right_cb.contrast = -1.*right_cb.contrast
    left_cb.draw()
    right_cb.draw()
    fixation.draw()
    text_stim.draw()
    win.flip()

    time.sleep(0.005)

    if side=='left':
        left_cb.contrast = -1.*left_cb.contrast
    elif side=='right':
        right_cb.contrast = -1.*right_cb.contrast
    left_cb.draw()
    right_cb.draw()
    fixation.draw()
    text_stim.draw()
    win.flip()

# seems to be a good thing to name it like this.
def hideCheckerboard(win,vis_contents):

    right_cb = vis_contents[0]
    left_cb=vis_contents[1]
    fixation=vis_contents[2]
    text_stim=vis_contents[3]
    fixation.draw()
    text_stim.draw()
    win.flip()
    new_vis_contents = [fixation,text_stim]
    return new_vis_contents

def showCheckerboard(win,vis_contents):

    right_cb = vis_contents[0]
    left_cb=vis_contents[1]
    fixation=vis_contents[2]
    text_stim=vis_contents[3]
    left_cb.draw()
    right_cb.draw()
    fixation.draw()
    text_stim.draw()
    new_vis_contents = [right_cb,left_cb,fixation,text_stim]
    return new_vis_contents
    

def textFlip(win,vis_contents):
    # well - this could use some improvements - in conceptualization.
    # the checkerboard_hidden could be done better.
    # that's what you get when you are programming quick -n- dirty.
    for item in vis_contents:
        item.draw()
    win.flip()


# Initialize components for Routine "end"
endClock = core.Clock()
end_text = visual.TextStim(win=win, name='end_text',
    text='This was the end - Thank you!',
    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "do_video"-------
t = 0
do_videoClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
#for i in range(0,100):
 #   if i==0:
  #      p1=play_vis_stim(win, hit_times_8Hz, right_cb,left_cb,fixation,'left')
   #     p1.run()
    #time.sleep(0.1)

#p2=play_vis_stim(win, hit_times_8Hz, right_cb,left_cb,fixation,'right')
#p2.start()

#p3=play_vis_stim(win, hit_times_13Hz, right_cb,left_cb,fixation,'left')
#p3.start()
#p4=play_vis_stim(win, hit_times_13Hz, right_cb,left_cb,fixation,'right')
#p4.start()


# keep track of which components have finished
do_videoComponents = []
for thisComponent in do_videoComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "do_video"-------
while continueRoutine:
    # get current time
    t = do_videoClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_videoComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "do_video"-------
for thisComponent in do_videoComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "do_video" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "do_audio"-------
t = 0
do_audioClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
# a = play_audio_stim(sounds,'right',55)
# a.start()

# keep track of which components have finished
do_audioComponents = []
for thisComponent in do_audioComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "do_audio"-------
while continueRoutine:
    # get current time
    t = do_audioClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_audioComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "do_audio"-------
for thisComponent in do_audioComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "do_audio" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "do_letters"-------
t = 0
do_lettersClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat

# keep track of which components have finished
do_lettersComponents = []
for thisComponent in do_lettersComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "do_letters"-------
while continueRoutine:
    # get current time
    t = do_lettersClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_lettersComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "do_letters"-------
for thisComponent in do_lettersComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "do_letters" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "do_triggers"-------
t = 0
do_triggersClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat

eeg_resp = event.BuilderKeyResponse()

# keep track of which components have finished
do_triggersComponents = [select_eeg_system, eeg_resp]
for thisComponent in do_triggersComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "do_triggers"-------
while continueRoutine:
    # get current time
    t = do_triggersClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *select_eeg_system* updates
    if t >= 0.0 and select_eeg_system.status == NOT_STARTED:
        # keep track of start time/frame for later
        select_eeg_system.tStart = t
        select_eeg_system.frameNStart = frameN  # exact frame index
        select_eeg_system.setAutoDraw(True)
    
    # *eeg_resp* updates
    if t >= 0.0 and eeg_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        eeg_resp.tStart = t
        eeg_resp.frameNStart = frameN  # exact frame index
        eeg_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(eeg_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if eeg_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['1', '2', '3', 'space', 'esc'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            eeg_resp.keys = theseKeys[-1]  # just the last key pressed
            eeg_resp.rt = eeg_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_triggersComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "do_triggers"-------
for thisComponent in do_triggersComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if eeg_resp.keys in ['', [], None]:  # No response was made
    eeg_resp.keys=None
thisExp.addData('eeg_resp.keys',eeg_resp.keys)
if eeg_resp.keys != None:  # we had a response
    thisExp.addData('eeg_resp.rt', eeg_resp.rt)
thisExp.nextEntry()

# VERY exhaustive - can i do this better?
my_key_pressed = eeg_resp.keys
eeg_systems = {'1':'none', '2':'egi', '3':'bp'} # of course it is a comma - like everything in pyhton
eeg_system_used = eeg_systems[my_key_pressed]

print eeg_system_used
# the Routine "do_triggers" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "instr"-------
t = 0
instrClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_begin = event.BuilderKeyResponse()
# keep track of which components have finished
instrComponents = [instr_text, key_begin]
for thisComponent in instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instr"-------
while continueRoutine:
    # get current time
    t = instrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr_text* updates
    if t >= 0.0 and instr_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        instr_text.tStart = t
        instr_text.frameNStart = frameN  # exact frame index
        instr_text.setAutoDraw(True)
    
    # *key_begin* updates
    if t >= 0.0 and key_begin.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_begin.tStart = t
        key_begin.frameNStart = frameN  # exact frame index
        key_begin.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_begin.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_begin.status == STARTED:
        theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_begin.keys = theseKeys[-1]  # just the last key pressed
            key_begin.rt = key_begin.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instr"-------
for thisComponent in instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_begin.keys in ['', [], None]:  # No response was made
    key_begin.keys=None
thisExp.addData('key_begin.keys',key_begin.keys)
if key_begin.keys != None:  # we had a response
    thisExp.addData('key_begin.rt', key_begin.rt)
thisExp.nextEntry()
# the Routine "instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "main_routine"-------
t = 0
main_routineClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
start_time=time.time()

# to control for showing(or not(!)) the checkerboard, to it like this:
video_is_running = 0
video_was_running = 0
audio_is_running = 0
audio_was_running = 0


# draw (only) the fixation cross, now, using the function:
new_vis_contents=hideCheckerboard(win,vis_contents)

# control how/when audio and visual elements are created:
v_next = 0
a_next = 0


# just start a separate thread - that contain letters, and which switches the letter - in memory - once per second
# one the letter is changed - set a 'changed' flag appropriately (i.e., that I can query)
# inside this loop - just query this thread - ask it if it changed - if it did, update the letter (& 'flip' the window)
letter_switch_interval = 1.0 # seconds
letter_switch_probability = 0.15 # 15 % change of switching the 'wrong' way = subjects have to press.
# the letters list has been defined somewhere else (previously!)
lstream = letter_stream(letters_for_letter_stream,letter_switch_interval,letter_switch_probability)
lstream.start()


while True:
    current_time=time.time() - start_time
    tasks=[]
    for item in all_timings:
        if current_time > item[0] and current_time < item[1]:
            tasks.append([item[2], item[3]])
    
    # keep track of them over here (!) - so thay they are (properly!!!) reset!
    video_is_running = 0
    audio_is_running = 0


    for task in tasks:
    
        action = task[0]
        options = task[1]
    
        # set the is_now_running to: zero - so that at the end of this loop, the is_now_running == 1 whenever a checkerboard vis_stim is present.

        if action=='video':

           # only set this to 1 if there is a task - 'video' in the task stack.
            video_is_running = 1

            # only set the checkerboard to true if it was off, first.
            if not video_was_running:
                print(' -- ENABLE CHECKERBOARD')
                new_vis_contents = showCheckerboard(win,vis_contents)


            # only create the v_next, if its value is not the (int) 0 value - so do THIS at first iteration of the block.
            # so - at the start; make an thread - and start it - and make a new thread just after that, just in case
            if v_next==0:
                v_current = play_vis_stim(vis_times,options[0],options[1])
                v_current.start()
                v_next = play_vis_stim(vis_times,options[0],options[1])
            else:
                # when NOT at the start - cycle to the next one - start it - prepare the new one already.
                # only start up the visual new thread once the current one is done (IF the task has a video element in it)
                if not v_current.isAlive():     
                    v_current=v_next
                    v_current.start()
                    v_next = play_vis_stim(vis_times,options[0],options[1])


        # handle the 'audio:
        if action=='audio':

            # mark audio is running(now)
            audio_is_running = 1


            # same handling for audio.
            if a_next==0:
                a_current=play_audio_stim(sounds,options[0],options[1])
                a_current.start()
                a_next=play_audio_stim(sounds,options[0],options[1])
            else:
                if not a_current.isAlive():                
                    a_current = a_next
                    a_current.start()
                    a_next=play_audio_stim(sounds,options[0],options[1])
                    


    # break the main loop if time is over:
    if current_time > max_time:
        # a graceful exit for the thread which normally wouldn't end...
        lstream.setStop()
        break



    # do the check here for either showing, or hiding, the checkerboards. Probably I can also ask for which elements are in the current visual stimulus.
    # need pygame manual for that...
    if video_was_running and not video_is_running:
        print(' -- DISABLE CHECKERBOARD')
        new_vis_contents = hideCheckerboard(win,vis_contents)

    
    # reset the video and/or audio stimuli:
    if not video_is_running:
        v_next = 0
    if not audio_is_running:
        a_next = 0


    # check if the visual thread is running, if so:
    # sort of assumes that there are checkerboard!
    if video_is_running:
        if v_current.queryFlash():
            # do the flash
            side = v_current.getSide()
            doFlash(win,vis_contents,side)

            # reset the flash value - and continue:
            v_current.resetFlash()


   # to keep track, do it like this:
    video_was_running = video_is_running
    audio_was_running = audio_is_running

    time.sleep(0.0005) # be kind to the computer - we won't need crazy timing accuracy - just accurate markers.



    # resolve letter stream.
    if lstream.queryFlag():
        letter = lstream.getLetter()
        text_stim.text=letter
        text_stim.text=text_stim.text # according to suggestion??
        textFlip(win,new_vis_contents)
        

    # ADD-ON which only works in psychopy?
    # enable key break...
    # do the key
    if event.getKeys(keyList=["escape"]):
        lstream.setStop()
        core.quit()
        continueRoutine=False

#    key = event.getKeys() # \also check for a keyboard trigger (any key) 
#    if len(key) > 0:
#       if not key == ['space']:
#          pass
#     else:
#         if key == ['escape']: core.quit() #  escape allows us to exit
#        continueRoutine = False


# keep track of which components have finished
main_routineComponents = []
for thisComponent in main_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "main_routine"-------
while continueRoutine:
    # get current time
    t = main_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in main_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "main_routine"-------
for thisComponent in main_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "main_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
end_key = event.BuilderKeyResponse()
# keep track of which components have finished
endComponents = [end_text, end_key]
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "end"-------
while continueRoutine:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_text* updates
    if t >= 0.0 and end_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        end_text.tStart = t
        end_text.frameNStart = frameN  # exact frame index
        end_text.setAutoDraw(True)
    
    # *end_key* updates
    if t >= 0.0 and end_key.status == NOT_STARTED:
        # keep track of start time/frame for later
        end_key.tStart = t
        end_key.frameNStart = frameN  # exact frame index
        end_key.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(end_key.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if end_key.status == STARTED:
        theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            end_key.keys = theseKeys[-1]  # just the last key pressed
            end_key.rt = end_key.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if end_key.keys in ['', [], None]:  # No response was made
    end_key.keys=None
thisExp.addData('end_key.keys',end_key.keys)
if end_key.keys != None:  # we had a response
    thisExp.addData('end_key.rt', end_key.rt)
thisExp.nextEntry()
# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()






# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
