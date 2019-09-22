import RPi.GPIO as GPIO
import time
from PIL import Image
import requests
from io import BytesIO

THRESHOLD = 40
cx = 0
cy = 0
ControlPinAxisX = [7,11,13,15]
ControlPinAxisY = [8,10,12,16]

class PixelInfo:
    def __init__(self, color, px, py):
        self.color = color
        self.px = px
        self.py = py
        self.positioned = False


ForwardSeg = [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ]

BackSeg =[ [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
            [1,0,0,0] ]


def move_x_axis(grids):
    if grids > 0:
        move_x_axis_forward(grids)
    elif grids < 0:
        move_x_axis_backward(grids)


def move_y_axis(grids):
    if grids > 0:
        move_y_axis_forward(grids)
    elif grids < 0:
        move_y_axis_backward(grids)


def move_x_axis_forward(grids):
    move(ControlPinAxisX, ForwardSeg, grids)


def move_x_axis_backward(grids):
    move(ControlPinAxisX, BackSeg, grids)


def move_y_axis_forward(grids):
    move(ControlPinAxisY, ForwardSeg, grids)


def move_y_axis_backward(grids):
    move(ControlPinAxisY, BackSeg, grids)


def move(pins, movement_seg, grids):
    for i in range (512):
       for halfstep in range (8):
             for pin in range (4):
                GPIO.output (pins[pin], movement_seg[halfstep][pin])
                time.sleep (0.001)


def setup_pins(pin_set):
    GPIO.setmode(GPIO.BOARD)

    for pin in pin_set:
       GPIO.setup (pin, GPIO.OUT)
       GPIO.output (pin, 0)


def setup_stepper_pins():
    setup_pins(ControlPinAxisX)
    setup_pins(ControlPinAxisY)


def load_image_grid(imageUrl):

    response = requests.get(imageUrl)
    img = Image.open(BytesIO(response.content))
    pix = img.load()

    # calc_grid_size(pix, img.size[0])

    gridCount = 16.0
    gridXY = img.size

    gridW = gridXY[0] / gridCount
    gridH = gridXY[1] / gridCount

    sx = 0
    pix_list = list()

    while sx < gridCount:
        px = (gridW / 2) + (gridW * sx)
        sy = 0
        while sy < gridCount:
            py = (gridH / 2) + (gridH * sy)
            pix_info = PixelInfo(pix[px, py], sx, sy)
            pix_list.append(pix_info)
            sy = sy + 1
        sx = sx + 1
    return pix_list


def capture_camera_image():
    print 'loading from camera...'
    return 'X'


def read_bead_list_from_camera():
    jpeg_data = capture_camera_image()
    bead_list = list()
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 255, 255))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    bead_list.append((5, 5, 3))
    return bead_list



def drop_bead():
    print 'mechanical drop bead'


def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])


def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold


def move_to(x, y):
    dx = x - cx
    dy = y - cy
    move_by_delta(dx, dy)


def move_by_delta(dx, dy):
    global cx
    global cy
    cx = cx + dx
    cy = cy + dy

    print "Moved by {}, {} to {}, {}".format(dx,dy,cx,cy)


def place_beads(imageURL):
    mypix = load_image_grid(imageURL)
    beads_unplaced = len(mypix)

    while beads_unplaced > 0:
        beads_list = read_bead_list_from_camera()
        for bead in beads_list:
            bead_x = -1
            bead_y = -1

            if beads_unplaced == 0:
                break

            for pixpos in mypix:
                if not pixpos.positioned and is_similar(pixpos.color, bead, THRESHOLD):
                    print "Placing at {}, {}".format(pixpos.px, pixpos.py)
                    pixpos.positioned = True
                    bead_x = pixpos.px
                    bead_y = pixpos.py
                    move_to(bead_x, bead_y)
                    drop_bead()
                    beads_unplaced -= 1
                    print "Remaining {}".format(beads_unplaced)
		    break

            if bead_x == -1 or bead_y == -1:
                print "Rejected {}".format(bead)
                move_to(-100, -100)
                drop_bead()


setup_stepper_pins()
place_beads("https://i.pinimg.com/originals/ff/57/6b/ff576b08cb60574709084273a6403fb0.png")



