# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* python files required to turn your pi into a proton pack

### Required libraries ###
* written for python 2.7 on raspbian
* use pip to install RPi for GPIO and pygame for GPIO access and sound respectively
* use pip to install tornado for websockets to allow remote control of the pack via a phone

### Physical setup ###
* wire up your shift registers and LEDs. This library is configured for 14 LEDs as seen https://eus-www.sway-cdn.com/s/T8VNqgdMtSaoMvuF/images/lIJtbxtQRrg_hP
* edit the Runner file at the top for all parameters including music/sound files and pins used
* run ./PytonPackRunner.py to start manually
* you can also run Web/PytonPackWeb.py to start a web site that will allow basic pack controls like turning on/off and toggling music

### Automatic setup ###
* copy the grabosky file (call it what you want) into /etc/init.d/ on the system
* edit it to the path of the Runner
* run `update-rc.d grabosky defaults` to put it into startup