# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* python files required to turn your pi into a proton pack

### Required libraries ###
* written for python 2.7 on raspbian
* use pip to install RPi for GPIO, PiShiftPy, pygame for GPIO, shift registers, and sound respectively

### Physical setup ###
* wire up your shift registers and LEDs. This library is configured for 14 LEDs as seen graboskyc.tumblr.com
* edit the Runner file at the top for all parameters including music/sound files and pins used
* run ./Runner.py to start manually

### Automatic setup ###
* copy the grabosky file (call it what you want) into /etc/init.d/ on the system
* edit it to the path of the Runner
* run `update-rc.d grabosky defaults` to put it into startup