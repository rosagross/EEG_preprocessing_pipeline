"""
File in which the control of the belt and defines the functionalities for the vibrotactile oddball blocks is defined.
Functions:
- connect_to_USB
- disconnect_belt
- vibrotactile_oddball_ankle
- vibrotactile_oddball_waist
- vibrotactile_oddball_wrist
- start_trial
It also handles the connection between the belt and the computer via USB.
"""

from pybelt import classicbelt
import parallel
import random, time
import numpy as np

class VibrationController():
    """
    The VibrationController controls the connection to the feelSpace belt.
    It saves the number of the vibrotactile units and links it to its purpose.

    Parameters
    ----------
    ankle_vibomotor : int
        The number of the vibrotactile unit attached to the ankle.
    ankle_trigger : list
        List with trigger codes for the ankle condition.
    wrist_vibromotor : int
        The number of the vibrotactile unit attached to the wrist.
    wrist_trigger : list
        List with trigger codes for the wrist condition.
    waist_vibromotor_left : int
        Number of the vibrotactile unit attached to the left side of the waist.
    waist_vibromotor_right : int
        Number of the vibrotactile unit attached to the right side of the waist.
    waist_trigger : list
        List with trigger codes for the waist condition.
    trial_break : float
        The length of the break between stimuli presentations in seconds.
    trial_length : float
        Defines the length of the trial (each stimulus presentation) in seconds.

    Attributes
    ----------
    belt_controller : BeltController
        This is where we store the controller of the belt, that is defined in
        the pyBelt package.
    ankle_vibomotor : int
        Stores the vibrotactile unit ID for the ankle.
    ankle_trigger : list
        Stores trigger codes for the ankle condition.
    wrist_vibromotor : int
        Stores the vibrotactile unit ID for the ankle.
    wrist_trigger : list
        Stores trigger codes for the wrist condition.
    waist_vibromotor_left : int
        Stores the vibrotactile unit ID for the left waist.
    waist_vibromotor_right : int
        Stores the vibrotactile unit ID for the right waist.
    waist_trigger : list
        Stores trigger codes for the waist condition.
    trial_break : float
        Stores the length of the break between stimuli presentations in seconds.
    trial_length : float
        Stores the length of the trial (stimulus presentation) in seconds.
    """

    def __init__(self, ankle_vibromotor, ankle_trigger, wrist_vibromotor,
                wrist_trigger, waist_vibromotor_left, waist_vibromotor_right,
                waist_trigger, trial_break, trial_length):
        """Constructor that initializes the belt controller."""
        # Instantiate a belt controller
        self.belt_controller = classicbelt.BeltController(delegate=self)
        self.ankle_vibromotor = ankle_vibromotor
        self.ankle_trigger = ankle_trigger
        self.wrist_vibromotor = wrist_vibromotor
        self.wrist_trigger = wrist_trigger
        self.waist_vibromotor_left =  waist_vibromotor_left
        self.waist_vibromotor_right = waist_vibromotor_right
        self.waist_trigger = waist_trigger
        self.trial_break = trial_break
        self.trial_length = trial_length

    def connect_to_USB(self):
        """Connect the belt to the serial port (USB)"""
        # connect belt to usb serial port
        print("Connect belt via USB.")
        print("Mode of the belt: ", self.belt_controller.getBeltMode())
        self.belt_controller.connectBeltSerial()

    def disconnect_belt(self):
        """Disconnect belt from serial port (USB)"""
        self.belt_controller.disconnectBelt()

    def vibrotactile_oddball_ankle(self, trials, oddball_ratio):
        """
        Start oddball vibration pattern at the ankle.

        Parameters:
        ----------
        trials : int
            A decimal integer indicating the nr. of trials
        oddball_ratio : float
            Indicating the proportion of odd stimuli
        """
        # Output used as control option for the experimenter.
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

            self.start_trial(mode, [self.ankle_vibromotor], self.ankle_trigger)

            total_trial = np.delete(total_trial, 0)

            # break between trials
            time.sleep(self.trial_break)

        print('oddballs', oddball_count)
        print('standards', standard_count)


    def vibrotactile_oddball_wrist(self, trials, oddball_ratio):
        """
        Start oddball vibration pattern at the wrist.

        Parameters
        ----------
        trials : int
            A decimal integer indicating the nr. of trials
        oddball_ratio : float
            Indicating the proportion of odd stimuli
        """

        # Output used as control option for the experimenter.
        print('-----------------------------------')
        print('          VIBROTACTILE WRIST       ')
        print('-----------------------------------\n')

        # An array for each condition (zeros and ones) is initialized and joined
        # to one trial array, to randomly pick one trial item of one specific
        # condition in the trial generating for-loop.
        total_trial_standard = np.zeros(int(trials*(1-oddball_ratio)))
        total_trial_oddball = np.ones(int(trials*(oddball_ratio)))
        total_trial = np.concatenate([total_trial_oddball, total_trial_standard])

        # For-loop generating the trials
        for i in range(trials):

            # The trial item is randomly picked by shuffeling the array and
            # taking the first element.
            np.random.shuffle(total_trial)
            random_number = total_trial[0]

            if random_number==1:
                mode = "oddball"
            else:
                mode = "standard"

            # Execution of the odd or standard trial.
            self.start_trial(mode, [self.wrist_vibromotor], self.wrist_trigger)

            # The currently executed trial is deleted from the trial storing array
            # to keep the correct number of oddball and standard trials.
            total_trial = np.delete(total_trial, 0)

            # break between trials
            time.sleep(self.trial_break)


    def vibrotactile_oddball_waist(self, trials, oddball_ratio):
        """
        Start oddball vibration pattern at the waist.

        Parameters
        ----------
        trials : int
            A decimal integer indicating the nr. of trials
        oddball_ratio : float
            Indicating the proportion of odd stimuli
        """

        # Output used as control option for the experimenter.
        print('-----------------------------------')
        print('           VIBROTACTILE WAIST          ')
        print('-----------------------------------\n')


        total_trial_standard = np.zeros(int(trials*(1-oddball_ratio)))
        total_trial_oddball = np.ones(int(trials*(oddball_ratio)))
        total_trial = np.concatenate([total_trial_oddball, total_trial_standard])

        for i in range(trials):
            np.random.shuffle(total_trial)
            random_number = total_trial[0]

            if random_number==1:
                mode = "oddball"
                oddball_count += 1
            else:
                mode = "standard"
                standard_count += 1

            self.start_trial(mode, [self.waist_vibromotor_left, self.waist_vibromotor_right], self.waist_trigger)

            # The currently executed trial is deleted from the trial storing array
            # to keep the correct number of oddball and standard trials.
            total_trial = np.delete(total_trial, 0)

            # break between trials
            time.sleep(self.trial_break)

    def start_trial(self, mode, vibromotors, trigger_codes):
        """
        Either an oddball or a standard vibration starts.

        Parameters
        ----------
        mode : str
            "Standard" or "oddball" -> virbation of low or high intensity
        vibromotors : int
            Integer refering to the correct vibrating unit
        trigger_codes : list
            Trigger for the stimuli in the respective vibrotactile condition.
            The order is [oddball, standard, break]
        """

        if mode == "standard":
            self.belt_controller.vibrateAtPositions(vibromotors, trigger_codes[1], 1, 30)
            time.sleep(self.trial_length)
            self.belt_controller.stopVibration()

        elif mode == "oddball":

            # Vibrate a first time (trigger is set in classicbelt function)
            self.belt_controller.vibrateAtPositions(vibromotors, trigger_codes[0], 1, 100)
            time.sleep(self.trial_length)
            self.belt_controller.stopVibration()

        # Trigger break
        classicbelt.p.setData(trigger_codes[2])
        core.wait(0.01)
        classicbelt.p.setData(0)
