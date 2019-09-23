from PIL import Image
import requests
from io import BytesIO

THRESHOLD = 40
cx = 0
cy = 0

class PixelInfo:
    def __init__(self, color, px, py):
        self.color = color
        self.px = px
        self.py = py
        self.positioned = False


def calc_grid_size(pix, width):
    last_pixel = (-1, -1, -1)
    last_size = 0
    best_guess = width
    change_rec =0

    last_x = 0


    while last_x < width:
        current_pixel = pix[last_x, 4]
        if  is_similar(current_pixel, last_pixel, 10) :
            last_size = last_size + 1
        else:
            last_pixel = (current_pixel[0], current_pixel[1], current_pixel[2])
            if not is_similar(current_pixel, (0,0,0), 10) :
                best_guess = last_size
                change_rec = change_rec +1
            last_size = 0

        last_x = last_x + 1
    print("Best guess is {}".format(best_guess))
    print("Grid count guess {}, changes {}".format(width * 1.0 / (best_guess), change_rec))


def luminance(pixel):
    return (0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])


def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold


def read_bead_list():
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


def get_image_grid(imageUrl):

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
        print '------'
        px = (gridW / 2) + (gridW * sx)
        sy = 0
        while sy < gridCount:
            py = (gridH / 2) + (gridH * sy)
            pix_info = PixelInfo(pix[px, py], sx, sy)
            pix_list.append(pix_info)
            if is_similar(pix[px, py], (0, 0, 0), THRESHOLD):
                print 'black'
            elif is_similar(pix[px, py], (217, 21, 45), THRESHOLD):
                print 'red at {}, {}  the PXY {}, {}'.format(sx, sy, px, py)
            elif is_similar(pix[px, py], (255, 255, 255), THRESHOLD):
                print 'white'
            else:
                print '???'
            sy = sy + 1
        sx = sx + 1
    return pix_list


def move_to(x, y):
    dx = x - cx
    dy = y - cy
    move_by(dx, dy)


def move_by(dx, dy):
    global cx
    global cy
    cx = cx + dx
    cy = cy + dy
    print "Moved by {}, {} to {}, {}".format(dx,dy,cx,cy)

vega = 'https://i.pinimg.com/originals/24/b9/cb/24b9cb8f8b6079610653ef2919e6f82a.png'
peach = 'http://cdn.shopify.com/s/files/1/0822/1983/articles/mario-kart-princess-peach-pixel-art-pixel-art-mario-kart-video-game-nintendo-racing-princess-peach-pixel-8bit.png'
mushroom = 'https://i.pinimg.com/originals/ff/57/6b/ff576b08cb60574709084273a6403fb0.png'

mypix = get_image_grid(mushroom)
beads = read_bead_list()

for bead in beads:
    bead_x = -1
    bead_y = -1
    for pixpos in mypix:
        if not pixpos.positioned and is_similar(pixpos.color, bead, THRESHOLD):
            pixpos.positioned = True
            bead_x = pixpos.px
            bead_y = pixpos.py
            move_to(bead_x, bead_y)
            print "Placed at {}, {}".format(pixpos.px, pixpos.py)
            break
    if bead_x == -1 or bead_y == -1:
        print "Rejected {}".format(bead)
