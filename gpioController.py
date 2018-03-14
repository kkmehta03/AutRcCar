import RPi.GPIO as GPIO
import sys
import Tkinter as tk

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(03, GPIO.OUT) #back motor pin
    GPIO.setup(05, GPIO.OUT) #back motor pin
    GPIO.setup(07, GPIO.OUT) #left pin
    GPIO.setup(11, GPIO.OUT) #right pin
def forwardGPIO():
    GPIO.output(03,True)
    GPIO.output(05,False)
    clean()
def reverseGPIO():
    GPIO.output(03,False)
    GPIO.output(05,True)
    clean()
def rightGPIO():
    GPIO.output(07,False)
    GPIO.output(11,True)
    clean()
def leftGPIO():
    GPIO.output(07,True)
    GPIO.output(11,False)
    clean()
def forwardLeftGPIO():
    forwardGPIO()
    leftGPIO()
    clean()
def forwardRightGPIo():
    forwardGPIO()
    rightGPIO()
    clean()
def reverseLeftGPIO():
    reverseGPIO()
    leftGPIO()
    clean()
def reverseRightGPIO():
    reverseGPIO()
    rightGPIO()
    clean()
def clean():
    GPIO.cleanup()

def key_in(event):
    init()
    key_press = event.char
    sleep_time = 0.030

    if key_press.lower() == 'w':
        forwardGPIO()
    elif key_press.lower() == 'a':
        leftGPIO()
    elif key_press.lower() == 's':
        reverseGPIO()
    elif key_press.lower() == 'd':
        rightGPIO()
    elif key_press.lower() == 'w' && 'a':
        forwardLeftGPIO()
    elif key_press.lower() == 'w' && 'd':
        forwardRightGPIo()
    elif key_press.lower() == 's' && 'a':
        reverseLeftGPIO()
    elif key_press.lower() == 's' && 'd':
        reverseRightGPIO()
    else:
        clean()

command = tk.Tk()
command.bind('<KeyPress>', key_input)
command.mainloop()
