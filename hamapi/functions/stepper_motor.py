import RPi.GPIO as GPIO
import time


class StepperMotor:
    def __init__(self, control_pins, axis_name):
        self.control_pins = control_pins
        self.axis_name = axis_name

        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        self.forward_segments =  [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]

        self.backward_segments = [
            [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
            [1,0,0,0]
        ]

    def move_by(self, grids_to_move):
        if grids_to_move < 0:
            moves = abs(grids_to_move)
            for i in range(0, moves):
                print("Axis {} move forward {} ".format(self.axis_name, i))
                self.move_backwards()
        elif grids_to_move > 0:
            for i in range(0, grids_to_move):
                print("Axis {} move backwards {} ".format(self.axis_name, i))
                self.move_forwards()

    def move_forwards(self):
        self.move(self.control_pins, self.forward_segments,1)

    def partial_move_forwards(self, partial):
        self.move(self.control_pins, self.forward_segments, partial)

    def move_backwards(self):
        self.move(self.control_pins, self.backward_segments,1)

    def partial_move_backwards(self, partial):
        self.move(self.control_pins, self.backward_segments, partial)

    def move(self, pins, movement_seg, rotation_fragment):

        full_move = 512
        partial_move = full_move / rotation_fragment

        for i in range(partial_move):
            for half_step in range(8):
                for pin in range(4):
                    GPIO.output(pins[pin], movement_seg[half_step][pin])
                time.sleep(0.001)


def setup_pins():
    GPIO.setmode(GPIO.BOARD)


def reset_pins():
    GPIO.cleanup()
