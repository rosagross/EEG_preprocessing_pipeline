## Experiment code - Overview
The folder 'EEG_experiment' contains all files necessary for executing the experiment. The folder 'pybelt' serves for the connection of the belt via USB and predefines functions that control the belt.

### Structure of files
- Parameter
- Functions vibrotactile
- Functions visual
- Main experiment

#### Parameter
Parameters can be set by the experimenter.
The parameters are:
- Nr. of trials per block
- Nr. of identical blocks (we have 4 different oddball blocks and can choose how often we want to repeat the identical blocks as minimum)
- Intensity of oddball and standard stimulus in the vibrotactile condition
- Colour of standard and oddball stimulus in the visual oddball condition
- Duration of break between trials
- Duration of each trial

#### Functions
There are two classes that include the functionalities for the experiment.
There is one class where the visual oddball functions are implemented and another one for the vibrotactile oddball functions:
+ <code>vibrotactile_functions.py</code>
  - vibrotactile_oddball_wrist
  - vibrotactile_oddball_ankle
  - vibrotactile_oddball_waist
+ <code>visual_functions.py</code>
  - visual_oddball
  - fingertapping task

#### Experiment
In the experiment file <code>experiment_code.py</code> a class of the type 'Experiment' is defined and instantiated. Running the file will execute the experiment. Make sure to have a belt connected to your laptop.
- Set up the screen with psychoPy
- Instantiate belt controller
- Read in data from parameter file
- Blocks are executed in randomized order.
- Write the data into an experiment file

### Belt set up
The labels written on the belt do not fit the variables we have to put into the code.
We will use: (body part, real belt label, variable integer)
- wrist, 9, 7
- waist left, 8, 8
- waist right, 7, 9
- ankle, 4, 10
