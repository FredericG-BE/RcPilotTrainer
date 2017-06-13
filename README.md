# What is "RC Pilot Trainer"?
RcPilotTrainer is a trainer for Remote Control Airplane Pilots. 

In contradiction to a traditional simulator, this tool focusses on one particular challenge or remote-controlled plying: knowing what input to give to achieve the intended rotation. This is a simple task when the plane is flying away from you, but some inputs get inverted when the plane flies towards you or flies inverted or a combination of both.

The tool shows a plane in a random position for a second and then starts rotating around one of the planes axis. You are invited to make an input with your remote control to counteract this rotation. At startup, you can choose from what possible start positions the tool can start from (flat, inverted, ...) and on what axes you want to train (aileron, elevator or yaw). As the training progresses, the tool learns what conditions you are struggling with.

# How to install
The tool is written in [Python](http://www.python.org), a very popular programming language. One option is to install Python and required packages (wx, pygame and OpenGL) on you system. Choose "Clone or Download" on this page, store the files somewhere on your hard disk and that's it.

Another option is to unzip this file on your hard disk. This avoids any installation. However, today, this option is only available for Windows (10?) 64 bit systems. I am unsure sure it needs to be Windows 10 or if it will work fine on older versions of Windows too.

# What do you need?
You need a dongle so that you can connect your RC transmitter to your PC. You need a device that emulates a joystick (HID device). Those are meant for free open-source simulators; dongles that come with commercial simulators will typically not work. I use [this Orange RX dongle](https://hobbyking.com/en_us/dsmx-dsm2-protocol-usb-dongle.html). This is a wireless device for DSM/SDMX transmitters, but other dongles, possibly wired ones, will also work provided they present themselves as a joystick and are compatible with your transmitter.

