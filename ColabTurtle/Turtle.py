from IPython.display import display, HTML
import time
import math
import re

# Created at: 23rd October 2018
#         by: Tolga Atam

# Module for drawing classic Turtle figures on Google Colab notebooks.
# It uses html capabilites of IPython library to draw svg shapes inline.
# Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)

DEFAULT_WINDOW_SIZE = (800, 500)
DEFAULT_SPEED = 4
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'white'
DEFAULT_TURTLE_DEGREE = 270
DEFAULT_BACKGROUND_COLOR = 'black'
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 4
# all 140 color names that modern browsers support. taken from https://www.w3schools.com/colors/colors_names.asp
VALID_COLORS = ('black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue', 'darkturquoise', 'mediumspringgreen', 'lime', 'springgreen', 'aqua', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen', 'darkslategray', 'darkslategrey', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue', 'darkslateblue', 'mediumturquoise', 'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'rebeccapurple', 'mediumaquamarine', 'dimgray', 'dimgrey', 'slateblue', 'olivedrab', 'slategray', 'slategrey', 'lightslategray', 'lightslategrey', 'mediumslateblue', 'lawngreen', 'chartreuse', 'aquamarine', 'maroon', 'purple', 'olive', 'gray', 'grey', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown', 'darkseagreen', 'lightgreen', 'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'darkgrey', 'lightblue', 'greenyellow', 'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 'mediumvioletred', 'indianred', 'peru', 'chocolate', 'tan', 'lightgray', 'lightgrey', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 'crimson', 'gainsboro', 'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki', 'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon', 'antiquewhite', 'linen', 'lightgoldenrodyellow', 'oldlace', 'red', 'fuchsia', 'magenta', 'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white')
VALID_COLORS_SET = set(VALID_COLORS)
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">
        <rect width="100%" height="100%" fill="{background_color}"/>
        {lines}
        {turtle}
      </svg>
    """
TURTLE_SVG_TEMPLATE = """
      <g visibility={visibility} transform="rotate({degrees},{turtle_x},{turtle_y}) translate({turtle_x}, {turtle_y})">
        <circle stroke="{turtle_color}" stroke-width="3" fill="transparent" r="12" cx="0" cy="0"/>
        <polygon points="0,19 3,16 -3,16" style="fill:{turtle_color};stroke:{turtle_color};stroke-width:2"/>
      </g>
    """

SPEED_TO_SEC_MAP = {1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18, 7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02, 11: 0.01, 12: 0.001, 13: 0.0001}


# helper function that maps [1,13] speed values to ms delays
def _speedToSec(speed):
    return SPEED_TO_SEC_MAP[speed]


turtle_speed = DEFAULT_SPEED

is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size = DEFAULT_WINDOW_SIZE
turtle_pos = (DEFAULT_WINDOW_SIZE[0] // 2, DEFAULT_WINDOW_SIZE[1] // 2)
turtle_degree = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH

drawing_window = None


# construct the display for turtle
def initializeTurtle(initial_speed=DEFAULT_SPEED, initial_window_size=DEFAULT_WINDOW_SIZE):
    global window_size
    global drawing_window
    global turtle_speed
    global is_turtle_visible
    global pen_color
    global turtle_pos
    global turtle_degree
    global background_color
    global is_pen_down
    global svg_lines_string
    global pen_width

    if isinstance(initial_speed,int) == False or initial_speed not in range(1, 14):
        raise ValueError('initial_speed must be an integer in interval [1,13]')
    turtle_speed = initial_speed

    if not (isinstance(initial_window_size, tuple) and len(initial_window_size) == 2 and isinstance(
            initial_window_size[0], int) and isinstance(initial_window_size[1], int)):
        raise ValueError('window_size must be a tuple of 2 integers')

    window_size = initial_window_size

    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    pen_color = DEFAULT_PEN_COLOR
    turtle_pos = (window_size[0] // 2, window_size[1] // 2)
    turtle_degree = DEFAULT_TURTLE_DEGREE
    background_color = DEFAULT_BACKGROUND_COLOR
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH

    drawing_window = display(HTML(_generateSvgDrawing()), display_id=True)


# helper function for generating svg string of the turtle
def _generateTurtleSvgDrawing():
    if is_turtle_visible:
        vis = 'visible'
    else:
        vis = 'hidden'

    return TURTLE_SVG_TEMPLATE.format(turtle_color=pen_color, turtle_x=turtle_pos[0], turtle_y=turtle_pos[1], \
                                      visibility=vis, degrees=turtle_degree - 90)


# helper function for generating the whole svg string
def _generateSvgDrawing():
    return SVG_TEMPLATE.format(window_width=window_size[0], window_height=window_size[1],
                               background_color=background_color, lines=svg_lines_string,
                               turtle=_generateTurtleSvgDrawing())


# helper functions for updating the screen using the latest positions/angles/lines etc.
def _updateDrawing():
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    time.sleep(_speedToSec(turtle_speed))
    drawing_window.update(HTML(_generateSvgDrawing()))


# helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
def _moveToNewPosition(new_pos):
    global turtle_pos
    global svg_lines_string

    # rounding the new_pos to eliminate floating point errors.
    new_pos = ( round(new_pos[0],3), round(new_pos[1],3) )

    start_pos = turtle_pos
    if is_pen_down:
        svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0], y1=start_pos[1], x2=new_pos[0], y2=new_pos[1], pen_color=pen_color, pen_width=pen_width)

    turtle_pos = new_pos
    _updateDrawing()


# makes the turtle move forward by 'units' units
def forward(units):
    if not (isinstance(units, int) and not isinstance(units, float)):
        raise ValueError('units must be a number.')

    alpha = math.radians(turtle_degree)
    ending_point = (turtle_pos[0] + units * math.cos(alpha), turtle_pos[1] + units * math.sin(alpha))

    _moveToNewPosition(ending_point)

fd = forward # alias

# makes the turtle move backward by 'units' units
def backward(units):
    if not isinstance(units, int) and not isinstance(units, float):
        raise ValueError('units must be a number.')
    forward(-1 * units)

bk = backward # alias
back = backward # alias


# makes the turtle move right by 'degrees' degrees (NOT radians)
def right(degrees):
    global turtle_degree

    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees must be a number.')

    turtle_degree = (turtle_degree + degrees) % 360
    _updateDrawing()

rt = right # alias

# makes the turtle face a given direction
def face(degrees):
    global turtle_degree

    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees must be a number.')

    turtle_degree = degrees % 360
    _updateDrawing()

setheading = face # alias
seth = face # alias

# makes the turtle move right by 'degrees' degrees (NOT radians, this library does not support radians right now)
def left(degrees):
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
        raise ValueError('degrees must be a number.')
    right(-1 * degrees)

lt = left

# raises the pen such that following turtle moves will not cause any drawings
def penup():
    global is_pen_down

    is_pen_down = False
    # TODO: decide if we should put the timout after lifting the pen
    # _updateDrawing()

pu = penup # alias
up = penup # alias

# lowers the pen such that following turtle moves will now cause drawings
def pendown():
    global is_pen_down

    is_pen_down = True
    # TODO: decide if we should put the timout after releasing the pen
    # _updateDrawing()

pd = pendown # alias
down = pendown # alias

def isdown():
    return is_pen_down

# update the speed of the moves, [1,13]
# if argument is omitted, it returns the speed.
def speed(speed = None):
    global turtle_speed

    if speed is None:
        return turtle_speed

    if speed not in range(1, 14):
        raise ValueError('speed must be an integer in the interval [1,13].')
    turtle_speed = speed
    # TODO: decide if we should put the timout after changing the speed
    # _updateDrawing()


# move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(x):
    if not isinstance(x, int) and not isinstance(x, float):
        raise ValueError('new x position must be a number.')
    if not x >= 0:
        raise ValueError('new x position must be non-negative.')
    _moveToNewPosition((x, turtle_pos[1]))


# move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(y):
    if not isinstance(y, int) and not isinstance(y, float):
        raise ValueError('new y position must be a number.')
    if not y >= 0:
        raise ValueError('new y position must be non-negative.')
    _moveToNewPosition((turtle_pos[0], y))


def home():
    global turtle_degree

    turtle_degree = DEFAULT_TURTLE_DEGREE
    _moveToNewPosition( (window_size[0] // 2, window_size[1] // 2) ) # this will handle updating the drawing.

# retrieve the turtle's currrent 'x' x-coordinate
def getx():
    return(turtle_pos[0])

xcor = getx # alias

# retrieve the turtle's currrent 'y' y-coordinate
def gety():
    return(turtle_pos[1])

ycor = gety # alias

# retrieve the turtle's current position as a (x,y) tuple vector
def position():
    return turtle_pos

pos = position # alias

# retrieve the turtle's current angle
def getheading():
    return turtle_degree

heading = getheading # alias

# move the turtle to a designated 'x'-'y' coordinate
def goto(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('the tuple argument must be of length 2.')

        y = x[1]
        x = x[0]

    if not isinstance(x, int) and isinstance(x, float):
        raise ValueError('new x position must be a number.')
    if not x >= 0:
        raise ValueError('new x position must be non-negative')
    if not isinstance(y, int) and  not isinstance(y, float):
        raise ValueError('new y position must be a number.')
    if not y >= 0:
        raise ValueError('new y position must be non-negative.')
    _moveToNewPosition((x, y))

setpos = goto # alias
setposition = goto # alias

# switch turtle visibility to ON
def showturtle():
    global is_turtle_visible

    is_turtle_visible = True
    _updateDrawing()

st = showturtle # alias

# switch turtle visibility to OFF
def hideturtle():
    global is_turtle_visible

    is_turtle_visible = False
    _updateDrawing()

ht = hideturtle # alias

def isvisible():
    return is_turtle_visible

def _validateColorString(color):
    if color in VALID_COLORS_SET: # 140 predefined html color names
        return True
    if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
        return True
    if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
        return True
    return False

def _validateColorTuple(color):
    if len(color) != 3:
        return False
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        return False
    if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
        return False
    return True

def _processColor(color):
    if isinstance(color, str):
        color = color.lower()
        if not _validateColorString(color):
            raise ValueError('color is invalid. it can be a known html color name, 3-6 digit hex string or rgb string.')
        return color
    elif isinstance(color, tuple):
        if not _validateColorTuple(color):
            raise ValueError('color tuple is invalid. it must be a tuple of three integers, which are in the interval [0,255]')
        return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'

# change the background color of the drawing area
def bgcolor(color):
    global background_color

    if color is None:
        return background_color
    elif c2 is not None:
        if c2 is None:
            raise ValueError('if the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    background_color = _processColor(color)
    _updateDrawing()


# change the color of the pen
def color(color = None, c2 = None, c3 = None):
    global pen_color

    if color is None:
        return pen_color
    elif c2 is not None:
        if c2 is None:
            raise ValueError('if the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    pen_color = _processColor(color)
    _updateDrawing()

pencolor = color

# change the width of the lines drawn by the turtle, in pixels
# if the function is called without arguments, it returns the current width
def width(width = None):
    global pen_width

    if width is None:
        return pen_width
    else:
        if not isinstance(width, int):
            raise ValueError('new width position must be an integer.')
        if not width > 0:
            raise ValueError('new width position must be positive.')

        pen_width = width
        # TODO: decide if we should put the timout after changing the pen_width
        # _updateDrawing()

pensize = width

# calculate the distance between the turtle and a given point
def distance(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('the tuple argument must be of length 2.')

        y = x[1]
        x = x[0]

    if not isinstance(x, int) and isinstance(x, float):
        raise ValueError('new x position must be a number.')
    if not x >= 0:
        raise ValueError('new x position must be non-negative')
    if not isinstance(y, int) and  not isinstance(y, float):
        raise ValueError('new y position must be a number.')
    if not y >= 0:
        raise ValueError('new y position must be non-negative.')

    if not isinstance(point, tuple) or len(point) != 2 or (not isinstance(point[0], int) and not isinstance(point[0], float)) or (not isinstance(point[1], int) and not isinstance(point[1], float)):
        raise ValueError('the vector given for the point must be a tuple with 2 numbers.')

    return round(math.sqrt( (turtle_pos[0] - x) ** 2 + (turtle_pos[1] - y) ** 2 ), 4)

# clear any text or drawing on the screen
def clear():
    global svg_lines_string

    svg_lines_string = ""
    _updateDrawing()

def write(obj, **kwargs):
    # NOT IMPLEMENTED YET. PLACEHOLDER FUNCTION FOR COMPATIBILITY WITH THE TRADITIONAL TURTLE LIBRARY
    print('Warning: write() is a no-op in this library.')

def shape(shape=None):
    # NOT IMPLEMENTED YET. THE ONLY POSSIBLE SHAPE IS CIRCLE FOR NOW.
    print('Warning: shape() is a no-op in this library.')
    if shape is None:
        return 'circle'
