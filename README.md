# What is "RC Pilot Trainer"?
RcPilotTrainer is a trainer for Remote Control Airplane Pilots. 

In contradiction to a traditional simulator, this tool focusses on one particular challenge or remote-controlled plying: knowing what input to give to achieve the intended rotation. This is a simple task when the plane is flying away from you, but some inputs get inverted when the plane flies towards you or flies inverted or a combination of both.

I created this tool because I hope I will progress faster on this particular aspect than with a regular simulator. 

![Screenshot](https://github.com/FredericG-BE/RcPilotTrainer/blob/master/Images/Screenshot.jpg)

The tool shows a plane in a random position for a second and then starts rotating around one of the planes axis. You are invited to make an input with your remote control to counteract this rotation. At startup, you can choose from what possible start positions the tool can start from (flat, inverted, ...) and on what axes you want to train (aileron, elevator or yaw). As the training progresses, the tool learns what conditions you are struggling with.

# How to install
The tool is written in [Python](http://www.python.org), a very popular programming language. One option is to install Python and required packages (wx, pygame and OpenGL) on you system. Choose "Clone or Download" on this page, store the files somewhere on your hard disk and that's it. Start __RcPilotTrainer.py__ 

There is an option which does not require you to intall anything. Using a tool called "PyInsatller" all required files where collected and zipped. You can just unzip in a directory on you PC and this should work. Today I have only made such a zip-file for Windows 10 64 bit systems. [The ZIP-file can be found here](http://rc-flight.be/RcCtrlTrainer/Win10_64/latest/RcPilotTrainer.zip) You need to start __RcPilotTrainer.exe__

# What else do you need?
You need a dongle so that you can connect your RC transmitter to your PC. You need a device that emulates a joystick (HID device). Those are meant for free open-source simulators; dongles that come with commercial simulators will typically not work. I use [this Orange RX dongle](https://hobbyking.com/en_us/dsmx-dsm2-protocol-usb-dongle.html). This is a wireless device for DSM/SDMX transmitters, but other dongles, possibly wired ones, will also work provided they present themselves as a joystick and are compatible with your transmitter.

