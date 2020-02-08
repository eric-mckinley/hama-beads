from functions.stepper_motor import StepperMotor
from functions.stepper_motor import reset_pins
from functions.stepper_motor import setup_pins
import time

setup_pins()


x_axis_stepper_motor = StepperMotor([7,11,13,15], "X")
y_axis_stepper_motor = StepperMotor([31,33,35,37], "Y")

time.sleep(3.0)

for x in range(8) :
    y_axis_stepper_motor.partial_move_backwards(0.667)

# y_axis_stepper_motor.partial_move_forwards(1)
# y_axis_stepper_motor.partial_move_forwards(1)

reset_pins()
