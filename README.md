# oscilloscope_embedded_system

This project implements an oscilloscope (embedded system) in Python on a simulator and on an IoT module. The module consists of a microcontroller board with diverse functionalities and interfaces, capable of functioning as an oscilloscope with software developed specifically for this purpose.

## Menu

  - [**Code**](#code)
  - [**Scripts**](#scripts)
  - [**Functionalities**](#functionalities)
  - [**Report**](#report)
   
## Code

The file `main.py` contains the main project, while the other files pertain to the simulator itself, including `.dat` files used in the simulator and examples.

## Scripts

There is a MATLAB script used to calibrate the IoT module, which obtains the equation of a linear regression. The parameters from this equation are used in the `main.py` file.

## Functionalities

A oscilloscope is implemented with the `main.py` file which does the following:

1. Initialize the display by clearing it.

2. Draw the grid, the scales, and the WiFi icon.

3. Read values from the ADC, convert them to voltages, and display the waveform on the grid.

4. Wait for the user to press a button:

   4.1. Button 1 quick click (11) – Return to step 1, starting a new reading and displaying the waveform (function of time).

   4.2. Button 1 long click (12) – Email the points obtained in step 3 and return to step 4, as a table with two columns, where the first column is time in seconds and the second is voltage in volts.

   4.3. Button 1 double click (13) – Clear the display and present the values of the measurement set described later.

   4.4.  Button 2 quick click (21) – Change the vertical scale, moving to the next scale in a circular manner (if on the first scale of 1V/div, move to 2V/div and so on, and if on the last, return to the first) and follow step 1.

   4.5. Button 2 long click (22) – Change the horizontal scale, moving to the next scale in a circular manner (if on the first scale of 5ms/div, move to 10ms/div and so on, and if on the last, return to the first) and follow step 1.

   4.6. Button 2 double click (23) – Calculate the Fourier transform of the waveform obtained in the last reading and graphically display the spectrum (function of frequency).

## Report

A written report (as well as the LaTeX source code) is included in this repository, which provides a detailed explanation of the project and demonstrates its validation on both the simulator and the IoT module.
