##BCI Training Protocol

This Training Interface is meant to be used with the OpenBCI to record EEG data. It tags time intervals and saves the 8-channels in a CSV file.

It was created using Pygame, a 2D library in Python, during the Brainihack on May 2014. We worked with the OpenBCI team and tried to create a system to control robots with 5 simple commands:

1. Up
2. Left
3. Right
4. Base (neutral brain state)

It was designed to use motor imagery and color in order to extract as many features as possible (so there is more information to machine learn on).

My friend Pierre Karashchuk was responsible for doing the Machine Learning and and Conor Russomanno hacked the RadioShack robot controllers to control it from the computer.

The project was never finished because of time constraints (the ML part), but we could control the robot with EMG.

