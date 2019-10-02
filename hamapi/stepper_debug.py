from functions.stepper_motor import StepperMotor
from functions.stepper_motor import reset_pins
from functions.stepper_motor import setup_pins

setup_pins()


x_axis_stepper_motor = StepperMotor([7,11,13,15], "X")
y_axis_stepper_motor = StepperMotor([31,33,35,37], "Y")

x_axis_stepper_motor.partial_move_backwards(4)
x_axis_stepper_motor.partial_move_forwards(2)
x_axis_stepper_motor.partial_move_backwards(8)
x_axis_stepper_motor.partial_move_backwards(2)

y_axis_stepper_motor.partial_move_backwards(4)
y_axis_stepper_motor.partial_move_forwards(2)
y_axis_stepper_motor.partial_move_backwards(8)
y_axis_stepper_motor.partial_move_backwards(2)

reset_pins()
