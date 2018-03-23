# AutRcCar
This is an autonomous RC car using Raspberry Pi model 3 B.
# Components:
1. Raspberry Pi 3 B,
2. Pi camera,
3. L293d motor driver,
4. Old RC car or 2 DC motors and wheels,
5. 9V battery for the motors,
6. Power Bank for the raspberry pi.

# Software:
The flask folder contains all the required files to control the pi car on any device (connected to the same network) using a browser, while streaming the camera data.
SSH into your raspberry pi and go to the flask folder.
Run python app.py and open the browser on another device. Type in your raspberry pi's IP address:5000 (which is the default port. Can be changed.)
