import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BOARD)

ControlPinAxisX = [7,11,13,15]
ControlPinAxisY = [31,33,35,37]

ForwardSeg =  [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ]

BackSeg = [ [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
            [1,0,0,0] ]

def move_x_axis_forward():
    move(ControlPinAxisX, ForwardSeg)

def move_x_axis_backward():
    move(ControlPinAxisX, BackSeg)

def move_y_axis_forward():
    move(ControlPinAxisY, ForwardSeg)

def move_y_axis_backward():
    move(ControlPinAxisY, BackSeg)

def move(pins, movement_seg):
    for i in range (512):
       for halfstep in range (8):
             for pin in range (4):
                GPIO.output (pins[pin], movement_seg[halfstep][pin])
                time.sleep (0.001)

def setupPins(pin_set):
    for pin in pin_set:
       GPIO.setup (pin, GPIO.OUT)
       GPIO.output (pin, 0)

def setupStepperPins():
    setupPins(ControlPinAxisX)
    setupPins(ControlPinAxisY)

setupStepperPins()
time.sleep (2.0)
move_x_axis_forward()

time.sleep (1.0)
move_y_axis_forward()

time.sleep (1.0)
move_x_axis_backward()

time.sleep (1.0)
move_y_axis_backward()

GPIO.cleanup()
