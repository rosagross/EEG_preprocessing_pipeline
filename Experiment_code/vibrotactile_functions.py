"""
Class that controls the belt and defines the functionalities for the vibrotactile oddball blocks.
Functions:
- vibrotactile_oddball_ankle
- vibrotactile_oddball_waist
- vibrotactile_oddball_wrist
"""

from pybelt import classicbelt
import parallel
from psychopy import visual, event, data, logging, core
import random, time
import numpy as np

class VibrationController():

    def __init__(self, ankle_vibromotor, wrist_vibromotor, waist_vibromotor_left, waist_vibromotor_right, trial_break):
        """Constructor that initializes the belt controller."""
        # Instantiate a belt controller
        self.belt_controller = classicbelt.BeltController(delegate=self)
        self.ankle_vibromotor = ankle_vibromotor
        self.wrist_vibromotor = wrist_vibromotor
        self.waist_vibromotor_left =  waist_vibromotor_left
        self.waist_vibromotor_right = waist_vibromotor_right
        self.trial_break = trial_break

    def connect_to_USB(self):
        """Connect the belt to the serial port (USB)"""
        # connect belt to usb serial port
        print("Connect belt via USB.")
        print("Mode of the belt: ", self.belt_controller.getBeltMode())
        self.belt_controller.connectBeltSerial()

    def disconnect_belt(self):
        self.belt_controller.disconnectBelt()

    def vibrotactile_oddball_ankle(self, trials, oddball_ratio):
        """Start oddball vibration pattern at the ankle."""
        print('-----------------------------------')
        print('           VIBROTACTILE ANKLE          ')
        print('-----------------------------------\n')

        total_trial_standard = np.zeros(int(trials*(1-oddball_ratio)))
        total_trial_oddball = np.ones(int(trials*(oddball_ratio)))
        total_trial = np.concatenate([total_trial_oddball, total_trial_standard])

        oddball_count = 0
        standard_count = 0

        for i in range(trials):

            np.random.shuffle(total_trial)
            random_number = total_trial[0]

            if random_number==1:
                mode = "oddball"
                oddball_count += 1
            else:
                mode = "standard"
                standard_count += 1

            print('MODE (standard or oddball): ', mode)

            self.start_trial(mode, [self.ankle_vibromotor], 9, 10, 11, 12, 22)


            total_trial = np.delete(total_trial, 0)


            # break between trials
            time.sleep(self.trial_break)

        print('oddballs', oddball_count)
        print('standards', standard_count)

    def vibrotactile_oddball_wrist(self, trials, oddball_ratio):
        """Start oddball vibration pattern at the wrist."""
        print('-----------------------------------')
        print('          VIBROTACTILE WRIST         ')
        print('-----------------------------------\n')

        total_trial_standard = np.zeros(int(trials*(1-oddball_ratio)))
        total_trial_oddball = np.ones(int(trials*(oddball_ratio)))
        total_trial = np.concatenate([total_trial_oddball, total_trial_standard])

        oddball_count = 0
        standard_count = 0

        for i in range(trials):

            np.random.shuffle(total_trial)
            random_number = total_trial[0]

            if random_number==1:
                mode = "oddball"
                oddball_count += 1
            else:
                mode = "standard"
                standard_count += 1

            print('MODE (standard or oddball): ', mode)

            self.start_trial(mode, [self.wrist_vibromotor], 5, 6, 7, 8, 23)

            total_trial = np.delete(total_trial, 0)

            # break between trials
            time.sleep(self.trial_break)

        print('oddballs', oddball_count)
        print('standards', standard_count)


    def vibrotactile_oddball_waist(self, trials, oddball_ratio):
        """Start oddball vibration pattern at the waist."""
        print('-----------------------------------')
        print('           VIBROTACTILE WAIST          ')
        print('-----------------------------------\n')


        total_trial_standard = np.zeros(int(trials*(1-oddball_ratio)))
        total_trial_oddball = np.ones(int(trials*(oddball_ratio)))
        total_trial = np.concatenate([total_trial_oddball, total_trial_standard])

        oddball_count = 0
        standard_count = 0

        for i in range(trials):
            np.random.shuffle(total_trial)
            random_number = total_trial[0]


            if random_number==1:
                mode = "oddball"
                oddball_count += 1
            else:
                mode = "standard"
                standard_count += 1

            print('MODE (standard or oddball): ', mode)

            self.start_trial(mode, [self.waist_vibromotor_left, self.waist_vibromotor_right], 1, 2, 3, 4, 24)

            total_trial = np.delete(total_trial, 0)

            # break between trials
            print('break')
            time.sleep(self.trial_break)

        print('oddballs', oddball_count)
        print('standards', standard_count)




    def start_trial(self, mode, vibromotors, trigger_oddball1, trigger_oddball2, trigger_standard, trigger_break, oddball_break):
        """
        Either an oddball or a standard vibration starts.
        The break between trials is included.
        In "standard" mode, the vibromotor only vibrates once for 1 second with a following
        break.
        In "oddball" mode, the vibromotor vibrates twice in 1 second, which feels like a
        perceivable different rythm.
        """

        if mode == "standard":
            self.belt_controller.vibrateAtPositions(vibromotors, trigger_standard, 1, 30)
            time.sleep(0.8)
            self.belt_controller.stopVibration()

        elif mode == "oddball":

            # This is the version for a high frequency oddball
            #self.belt_controller.pulseAtPositions(vibromotors, 20, 20, trigger_oddball1, channel_idx=1, intensity=80)
            #time.sleep(0.8)

            # Vibrate a first time (trigger is set in classicbelt function)
            self.belt_controller.vibrateAtPositions(vibromotors, trigger_oddball1, 1, 100)
            time.sleep(0.8)
            self.belt_controller.stopVibration()

            # Trigger break
            #classicbelt.p.setData(oddball_break)
            #core.wait(0.01)
            #classicbelt.p.setData(0)
            #time.sleep(0.10)

            # Vibrate a second time (trigger is set in classicbelt function)
            #self.belt_controller.vibrateAtPositions(vibromotors, trigger_oddball2, 1, 80)
            #time.sleep(0.35)
            #self.belt_controller.stopVibration()

        # Trigger break
        classicbelt.p.setData(trigger_break)
        core.wait(0.01)
        classicbelt.p.setData(0)
