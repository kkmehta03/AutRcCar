# AutRcCar
This is an autonomous RC car using Raspberry Pi model 3 B.
# Components:
1. Raspberry Pi 3 B,
2. Pi camera,
3. L293d motor driver,
4. Old RC car or 2 DC motors and wheels,
5. 9V battery for the motors,
6. Power Bank for the raspberry pi.

# Steps to train the car:
The flask folder contains all the required files to control the pi car from any device (connected to the same network) using a browser, while streaming the camera data.
1. SSH into your raspberry pi and go to the flask folder.
2. Run python app.py and open the browser on another device. Type in your raspberry pi's IP address:5000 (which is the default port. Can be changed.)
3. Drive your car around while recording the camera stream from RPi_Cam_Web_Interface cloned and installed from Github. Link - https://github.com/silvanmelchior/RPi_Cam_Web_Interface
4. Run "Opencv_vid2.py" - convert video to grayscale images and save it in "TrainingData" folder. (Branch - Edit3 contains all the code to use color images, instead of grayscale.)
5. Sort out the images of left direction into folder named "left", images of right direction into the folder named "Right" and so on.
6. Open up "Opencv_label.ipynb" Python notebook. Hit Shift+Enter to execute the first set of code, which converts all the images into numpy arrays and labels them according to the direction. 
left        -  [1 0 0 0]
forward     -  [0 1 0 0]
right       -  [0 0 1 0]
stop/reverse-  [0 0 0 1]
7. After labelling is done, the npz file is saved in the system, in folder called "Training_data_temp".
8. Load the file name of npz file and hit Shift+Enter for the next set of code to actually train the model. 
9. Model saved in mlp_xml folder as "mlp.xml".
# Steps to deploy the model on the pi:
1. Transfer the saved xml model to the pi. 
  -On Windows, use WinSCP software for really quick transfer of mlp.xml files. 
  -On linux, you can directly use scp command after SSH into pi.
2. cd into your directory where this repo is cloned.
3. Run Python3 Autodriver.py to run the car autonomously.
