"""
This file includes functions for the visual oddball part that used in the Experiment class.
- set_up_screen: sets up the screen where the fixation cross and later the stimulus is dispayed
- show_instructions : Shows instructions in the beginning and for every fingertapping task
- show_ready_screen :
- start_fingertapping_screen
- show_thank_you
- show_fixation_cross
- visual_oddball :
"""

from psychopy import visual, event, data, logging, core
import random, datetime, time
import parameter
import numpy as np
import csv
from pybelt import classicbelt # we need this to set the trigger

class ScreenController():
"""

Parameters
---------
color_standard : str
    The color of the frequently occuring circle stimulus.
color_oddball : str
    The color of the infrequently occuring circle stimulus.
trial_break : float
    Defines the length of the break between stimuli presentations in seconds.
trial_length : float
    Defines the length of the trial (each stimulus presentation) in seconds.
visual_trigger : list
    List of trigger codes for the stimuli in the visual oddball paradigm.

Attributes
----------
color_standard : str
    Stores color of the frequently occuring circle stimulus.
color_oddball : str
    Stores color of the infrequently occuring circle stimulus.
trial_break : float
    Stores the length of the break between stimuli presentations in seconds.
trial_length : float
    Stores the length of the trial (each stimulus presentation) in seconds.
visual_trigger : list
    Stores trigger codes for the stimuli in the visual oddball paradigm.
participant_ID : int
    Stores the ID of the current participant.
fingertapping_file_name : str
    Stores the name of the file that saves the fingertapping data.
win : Window (object of psychoPy library)
    Represents the window that is monitoring stimuli, text and fixation cross.
globalClock : Clock (object of core package)
    Stores the exact current time. Used for measuring reaction times in fingertapping.

Visual stimuli and text that will be presented during the experiment have to be
defined in the constructor directly.
"""

    def __init__(self, color_standard, color_oddball, trial_break, trial_length, visual_trigger):

        # set the color of the visual stimuli
        self.color_oddball = color_oddball
        self.color_standard = color_standard
        self.trial_break = trial_break
        self.trial_length = trial_length
        self.visual_trigger = visual_trigger

        # Used for saving fingertapping data into file
        self.participant_ID = parameter.participant_ID
        self.fingertapping_file_name = parameter.fingertapping_file_name

        # set window
        self.win = visual.Window([1920, 1080], units='height', winType='pyglet', fullscr=True)
        self.globalClock = core.Clock()

        #------------------------
        # Visual stimuli and text
        #------------------------
        self.instruction = visual.TextStim(self.win,
                text='Welcome to our experiment! \nPlease press any button if you are ready to start\n' \
                     'Please focus on the fixation cross in the middle of the screen.', height=0.05)

        self.fingertapping_instruction = visual.TextStim(self.win,
                 text='Fingertapping task: Press the keys following the sequence on the screen with your non-dominant hand.\n Repeat following the sequence until the sequence disappears.\n  Press any key if you are ready to start fingertapping', height=0.05)

        self.fingertapping_end = visual.TextStim(self.win,
                 text='Stop finger tapping', height=0.05)

        self.digit_sequence = [1, 2, 3, 4]

        self.ready_screen = visual.TextStim(self.win,
                 text='Please press any key if you are ready to continue the experiment. Please fixate on the fixation cross!', height=0.05)

        self.pause_screen = visual.TextStim(self.win,
                 text='Please wait', height=0.05)

        self.thank_you = visual.TextStim(self.win, text='Thanks for participating! :)', height=0.05)

        # fixation cross
        self.fixation = visual.ShapeStim(self.win,
                vertices=((0, -3), (0, 3), (0,0), (-3,0), (3, 0)),
                lineWidth=5,
                size=.01,
                closeShape=False,
                lineColor='black'
            )

        # initialize circle stimulus (colour doesn't matter here)
        self.circle_stim = visual.Circle(self.win,
                radius = 0.07,
                fillColor = 'cyan',
                lineColor = 'cyan'
            )

    def show_instructions(self):
        """
        Set up the screen for the experiment and show instructions.
        """
        self.instruction.draw()
        self.win.flip()
        event.waitKeys()

    def show_ready_screen(self):
        """
        Is shown between trials to check if participant is ready for the next block.
        """
        self.ready_screen.draw()
        self.win.flip()
        # Set trigger for showing ready screen
        classicbelt.p.setData(21)
        core.wait(0.01)
        classicbelt.p.setData(0)
        event.waitKeys()

    def start_fingertapping_screen(self, ft_round):
        """
        Set up the screen for the experiment and show instructions.

        Parameters
        ----------
        ft_round : int
            Tells us often (out of 4) we did the fingertapping task. This is to
            save the information in the fingertapping data file.
        """
        self.fingertapping_instruction.draw()
        self.win.flip()
        event.waitKeys()

        # Show the sequence for the finger tapping task
        random.shuffle(self.digit_sequence)
        new_sequence = self.digit_sequence[:]
        new_sequence.append(self.digit_sequence[0])
        fingertapping_sequence = visual.TextStim(self.win,
                  text= ' - '.join([str(number) for number in new_sequence]), height=0.05)
        fingertapping_sequence.draw()
        self.win.flip()

        # Set trigger for showing the sequence
        classicbelt.p.setData(17)
        core.wait(0.01)
        classicbelt.p.setData(0)

        tapping_Clock = core.Clock() #creates a clock time
        start_tapping_time = tapping_Clock.getTime() # gets time at this point

        file = open(self.fingertapping_file_name, 'a', newline ='')
        with file:
            header = ['KeysPressed', 'StartTappingTime', 'FingertappingRound', 'CorrectSequence', 'ParticipantID']
            writer = csv.DictWriter(file, fieldnames = header)

            if ft_round == 1:
                print("first tapping round")
                writer.writeheader()

            while True:

                if (tapping_Clock.getTime() - start_tapping_time) > 30:
                    "Stop fingertapping"
                    break

                keyPressed = event.getKeys(keyList=['1','2','3','4'], modifiers=False, timeStamped=tapping_Clock)

                if keyPressed:
                    print(keyPressed)
                    classicbelt.p.setData(18)
                    core.wait(0.01)
                    classicbelt.p.setData(0)
                    writer.writerow({header[0] : keyPressed[0][0],
                                     header[1] : keyPressed[0][1],
                                     header[2] : ft_round,
                                     header[3] : ''.join([str(j) for j in new_sequence]),
                                     header[4] : self.participant_ID})

        self.fingertapping_end.draw()
        self.win.flip()
        core.wait(3)

        classicbelt.p.setData(19)
        core.wait(0.01)
        classicbelt.p.setData(0)

        self.pause_screen.draw()
        self.win.flip()

        classicbelt.p.setData(20)
        core.wait(0.01)
        classicbelt.p.setData(0)
        event.waitKeys()


    def show_thank_you(self):
        """
        Show the last window for the experiment, where we thank the participants.
        After that, end the experiment.
        """
        self.thank_you.draw()
        self.win.flip()
        event.waitKeys()

        # end the experiment
        self.win.close()
        core.quit()


    def show_fixation_cross(self):
        """
        Show screen with fixation cross. This is needed during all vibrotactile oddball blocks
        as well as the finger tapping task.
        """
        # fixation cross
        self.fixation.draw()
        self.win.flip()

        # TRIGGER
        classicbelt.p.setData(16)
        core.wait(0.01)
        classicbelt.p.setData(0)


    def visual_oddball(self, trials, oddball_ratio):
        """
        Function that runs the trials of the visual oddball stimulus.

        Parameters
        ----------
        trials : int
            The number of trials in this condition (visual).
        oddball_ratio : float
            The frequency of displaying the oddball stimulus.
        """

        print('-----------------------------------')
        print('           VISUAL ODDBALL          ')
        print('-----------------------------------\n')

        total_trial_standard = np.zeros(int(trials*(1-oddball_ratio)))
        total_trial_oddball = np.ones(int(trials*(oddball_ratio)))
        total_trial = np.concatenate([total_trial_oddball, total_trial_standard])

        for i in range(trials):
            # fixation cross
            self.fixation.draw()
            self.win.flip()

            # TRIGGER
            classicbelt.p.setData(self.visual_trigger[2])
            core.wait(0.01)
            classicbelt.p.setData(0)

            # always pause some miliseconds after the stimulus is shown
            time.sleep(self.trial_break)

            # Change the color of the circle. This will be 30% pink=oddball and
            # 70% cyan for the baseline stimulus
            # create random number between 0 and 1
            np.random.shuffle(total_trial)
            random_number = total_trial[0]

            if random_number==1:
                col = self.color_oddball
            else:
                col = self.color_standard

            self.circle_stim = visual.Circle(self.win,
                    radius = 0.07,
                    fillColor = col,
                    lineColor = col
                )

            total_trial = np.delete(total_trial, 0)


            if col == "cyan":
                trigger_visual = self.visual_trigger[1]
            else:
                trigger_visual = self.visual_trigger[0]

            self.circle_stim.draw()
            self.win.flip()

            # TRIGGER
            classicbelt.p.setData(trigger_visual)
            core.wait(0.01)
            classicbelt.p.setData(0)

            # Show the circle for 800 ms
            core.wait(trial_length)
