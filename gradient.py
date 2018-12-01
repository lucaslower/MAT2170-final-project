"""
Gradient.py
by lucaslower

Generates a linear top-to-bottom gradient given two hex color codes
"""

import cImage
import math

start_color = input('Enter gradient start color (e.g. FFFFFF): ')
if start_color[0] == '#':
    start_color = start_color[1:]
while len(start_color) != 6:
    start_color = input('Hex color must be 6 characters: ')
    if start_color[0] == '#':
        start_color = start_color[1:]

end_color = input('Enter gradient end color (e.g. 000000): ')
if end_color[0] == '#':
    end_color = end_color[1:]
while len(end_color) != 6:
    end_color = input('Hex color must be 6 characters: ')
    if end_color[0] == '#':
        end_color = end_color[1:]

image_size = int(input('Image size (in pixels): '))

# create image
image_out = cImage.EmptyImage(image_size, image_size)
image_win = cImage.ImageWin("Computed Gradient", image_size, image_size)

# start RGB values
rgb_start = (int(start_color[:2], 16), int(start_color[2:4], 16), int(start_color[4:6], 16))

# end RGB values
rgb_end = (int(end_color[:2], 16), int(end_color[2:4], 16), int(end_color[4:6], 16))

print('START: ', rgb_start)
print('END: ', rgb_end)

# CALCULATE DIFFERENCES
diff = ( rgb_end[0] - rgb_start[0], rgb_end[1] - rgb_start[1], rgb_end[2] - rgb_start[2] )

print('DIFF: ', diff)

# GET MAX DIFFERENCE FOR TOP LEVEL LOOP
diff_max = 0
for color in diff:
    if abs(color) > diff_max:
        diff_max = abs(color)
        index_max = diff.index(color)

# GET RATIO OF MAX DIFF STEP SIZE TO IMAGE HEIGHT
step_ratio = diff_max/image_size

# CALCULATE STEP SIZES
r_step = step_ratio*(diff[0]/diff_max)
g_step = step_ratio*(diff[1]/diff_max)
b_step = step_ratio*(diff[2]/diff_max)

# LOOP THROUGH MAX DIFF AND STEP EACH COLOR
print(rgb_start)
cur_color = [rgb_start[0], rgb_start[1], rgb_start[2]]
for row in range(image_size):
    cur_color[0] = cur_color[0] + r_step
    cur_color[1] = cur_color[1] + g_step
    cur_color[2] = cur_color[2] + b_step
    # create pixel
    the_pixel = cImage.Pixel(math.floor(cur_color[0]), math.floor(cur_color[1]), math.floor(cur_color[2]))
    # loop horizontally
    for col in range(image_size):
        image_out.setPixel(col, row, the_pixel)

# draw image
image_out.draw(image_win)
image_win.exitOnClick()