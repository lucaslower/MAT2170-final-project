"""
State-based Data Visualizer --- Main program.
Crafted with care by Lucas Lower.
"""
import importlib.util, math
# import file_read
spec_file_read = importlib.util.spec_from_file_location('file_read', '/var/www/projects.lucaslower.com/us-map/modules/file_read.py')
file_read = importlib.util.module_from_spec(spec_file_read)
spec_file_read.loader.exec_module(file_read)
# import color_map
spec_color_map = importlib.util.spec_from_file_location('color_map', '/var/www/projects.lucaslower.com/us-map/modules/color_map.py')
color_map = importlib.util.module_from_spec(spec_color_map)
spec_color_map.loader.exec_module(color_map)
# import PIL
from PIL import Image, ImageDraw, ImageFont


# get file attributes from given number
def get_file_attributes(file_num):
    # file name map
    files = {1: 'legislators-current.csv', 2: 'starbucks.csv', 3: 'state-gsp-growth.csv', 4: 'state-water-area.csv'}
    # file title map
    file_titles = {
        1: 'Number of legislators (senators/representatives) per state',
        2: 'Number of Starbucks stores per state',
        3: 'Percent growth in GSP (Gross State Product) per state',
        4: 'Percent area of each state that is water'
    }
    # full path
    file_name = '/var/www/projects.lucaslower.com/us-map/data_files/' + files[file_num]
    # data type, state column if needed
    if file_num == 1:
        file_type = 2
        state_col = 5
    elif file_num == 2:
        file_type = 2
        state_col = 3
    else:
        file_type = 1
        state_col = None
    return (file_name, file_type, state_col, file_titles[file_num])


# parse hex colors --> RGB
def parse_color(hex_color):
    if hex_color[0] == '#':
        hex_color = hex_color[1:]
    return (int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


# generate map, pass back reachable URL
def generate_map(file_num, start_color, end_color):

    # get file name (and other attributes) from user's chosen file
    file_attr = get_file_attributes(file_num)

    # Generate R,G,B values from given hex codes
    print(start_color)
    print(end_color)
    rgb_start = parse_color(start_color)
    rgb_end = parse_color(end_color)
    rgb_diff = (rgb_end[0] - rgb_start[0], rgb_end[1] - rgb_start[1], rgb_end[2] - rgb_start[2])

    # read pixel map file (creates State() objects for each state)
    state_d = file_read.read_pixel_file()

    # read data file
    if file_attr[1] == 1:
        data = file_read.read_csv_file_raw(file_attr[0])
    elif file_attr[1] == 2:
        data = file_read.read_csv_file_frequency(file_attr[0], file_attr[2], state_d)

    # open state image
    im = Image.open('/var/www/projects.lucaslower.com/us-map/images/us_map.png')
    print(im.format, im.size, im.mode)

    # setup color map instance
    vals = data.values()
    print(max(vals), min(vals))
    cmap = color_map.ColorMap(rgb_end, rgb_start, min(vals), max(vals))

    # setup draw fonts
    fnt = ImageFont.truetype('/var/www/projects.lucaslower.com/us-map/fonts/anonpro.ttf', 55)
    title_fnt = ImageFont.truetype('/var/www/projects.lucaslower.com/us-map/fonts/anonpro.ttf', 65)
    draw = ImageDraw.Draw(im)

    # draw title text
    title_offset = draw.textsize(file_attr[3], font=title_fnt)//2
    draw.text((2301 - title_offset, 120), file_attr[3], font=title_fnt, fill=(0, 0, 0))

    for state in state_d:
        # get state data
        fill_color = cmap.compute_color(data[state])
        state_pixel = state_d[state].get_pixel()
        text_pixel = (state_pixel[0] - 20, state_pixel[1] - 20)
        # fill state with computed color
        ImageDraw.floodfill(im, state_pixel, fill_color, None, 30)
        # some states have 1 or more disconnected regions, let's handle that
        if state == 'MI':
            ImageDraw.floodfill(im, (2912,588), fill_color, None, 30)
        elif state == 'VA':
            ImageDraw.floodfill(im, (3916,1328), fill_color, None, 30)
        elif state == 'MD':
            ImageDraw.floodfill(im, (3616,1176), fill_color, None, 30)
        # why does hawaii need so many islands
        elif state == 'HI':
            ImageDraw.floodfill(im, (1308,2384), fill_color, None, 30)
            ImageDraw.floodfill(im, (1452,2440), fill_color, None, 30)
            ImageDraw.floodfill(im, (1553,2476), fill_color, None, 30)
            ImageDraw.floodfill(im, (1608,2513), fill_color, None, 30)
            ImageDraw.floodfill(im, (1252,2399), fill_color, None, 30)
            ImageDraw.floodfill(im, (1553,2505), fill_color, None, 30)
        # draw state label text
        draw.text(text_pixel, state, font=fnt, fill=(255 - fill_color[0], 255 - fill_color[1], 255 - fill_color[2]))

    # DRAW GRADIENT SCALE

    # set scale box coords
    top_left = (4140,1340)
    bot_right = (4280,2540)

    # calc height in px
    height = bot_right[1] - top_left[1]

    # get max color diff
    diff_max = 0
    for color in rgb_diff:
        if abs(color) > diff_max:
            diff_max = abs(color)

    # step size modifier
    step_mod = diff_max / height

    # calculate step sizes
    r_step = step_mod * (rgb_diff[0] / diff_max)
    g_step = step_mod * (rgb_diff[1] / diff_max)
    b_step = step_mod * (rgb_diff[2] / diff_max)

    # setup current color
    cur_color = [rgb_start[0], rgb_start[1], rgb_start[2]]

    # loop through rows
    for row in range(height):
        # change color by step
        cur_color[0] = cur_color[0] + r_step
        cur_color[1] = cur_color[1] + g_step
        cur_color[2] = cur_color[2] + b_step
        # setup coord list
        points = [(top_left[0],top_left[1]+row), (bot_right[0], top_left[1]+row)]
        # draw line across box
        draw.line(points, (math.floor(cur_color[0]), math.floor(cur_color[1]), math.floor(cur_color[2])), 1)

    # draw max and min text
    draw.text((4310, 1340), str(max(vals)), font=fnt, fill=(0, 0, 0))
    draw.text((4310, 2485), str(min(vals)), font=fnt, fill=(0, 0, 0))

    # image out
    im.save('/var/www/projects.lucaslower.com/us-map/generated/map.jpg')

    # passback url (if we stored more than 1 generated map this would make more sense
    # because we would store the path in DB and use the primary key as file name)
    return 'http://projects.lucaslower.com/us-map/generated/map.jpg'