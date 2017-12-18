# Count Down Switch Configuratior
A GUI to configure the count down switch device I designed.

## Description
This is a helper project for the project https://github.com/yrh79/count_down_switch_serial_config project, which sends commands to set the configuration of the count_down_switch via serial ports.

This is a GUI written in python. To compile it into a windows executable, please copy msvcp90.dll into the src folder and run make.bat (modify the path to python.exe as needed).

The application would try to discover the correct comport to use automatically.

Note: Ramdom crash on Linux is found, reason unknown yet. I'll try to figure out the reason and get it fix later on.
