from IPython.display import display, DisplayHandle, HTML
import time
import math
import re
from typing import Literal, overload

TurtleShape = Literal["turtle", "circle"]
TextAlign = Literal["left", "center", "right"]
FontType = Literal["bold", "italic", "underline", "normal"]

DEFAULT_WINDOW_SIZE = (800, 500)
DEFAULT_SPEED = 4
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = "white"
DEFAULT_TURTLE_DEGREE = 270
DEFAULT_BACKGROUND_COLOR = "black"
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 4
# all 140 color names that modern browsers support. taken from https://www.w3schools.com/colors/colors_names.asp
VALID_COLORS = (
    "black",
    "navy",
    "darkblue",
    "mediumblue",
    "blue",
    "darkgreen",
    "green",
    "teal",
    "darkcyan",
    "deepskyblue",
    "darkturquoise",
    "mediumspringgreen",
    "lime",
    "springgreen",
    "aqua",
    "cyan",
    "midnightblue",
    "dodgerblue",
    "lightseagreen",
    "forestgreen",
    "seagreen",
    "darkslategray",
    "darkslategrey",
    "limegreen",
    "mediumseagreen",
    "turquoise",
    "royalblue",
    "steelblue",
    "darkslateblue",
    "mediumturquoise",
    "indigo",
    "darkolivegreen",
    "cadetblue",
    "cornflowerblue",
    "rebeccapurple",
    "mediumaquamarine",
    "dimgray",
    "dimgrey",
    "slateblue",
    "olivedrab",
    "slategray",
    "slategrey",
    "lightslategray",
    "lightslategrey",
    "mediumslateblue",
    "lawngreen",
    "chartreuse",
    "aquamarine",
    "maroon",
    "purple",
    "olive",
    "gray",
    "grey",
    "skyblue",
    "lightskyblue",
    "blueviolet",
    "darkred",
    "darkmagenta",
    "saddlebrown",
    "darkseagreen",
    "lightgreen",
    "mediumpurple",
    "darkviolet",
    "palegreen",
    "darkorchid",
    "yellowgreen",
    "sienna",
    "brown",
    "darkgray",
    "darkgrey",
    "lightblue",
    "greenyellow",
    "paleturquoise",
    "lightsteelblue",
    "powderblue",
    "firebrick",
    "darkgoldenrod",
    "mediumorchid",
    "rosybrown",
    "darkkhaki",
    "silver",
    "mediumvioletred",
    "indianred",
    "peru",
    "chocolate",
    "tan",
    "lightgray",
    "lightgrey",
    "thistle",
    "orchid",
    "goldenrod",
    "palevioletred",
    "crimson",
    "gainsboro",
    "plum",
    "burlywood",
    "lightcyan",
    "lavender",
    "darksalmon",
    "violet",
    "palegoldenrod",
    "lightcoral",
    "khaki",
    "aliceblue",
    "honeydew",
    "azure",
    "sandybrown",
    "wheat",
    "beige",
    "whitesmoke",
    "mintcream",
    "ghostwhite",
    "salmon",
    "antiquewhite",
    "linen",
    "lightgoldenrodyellow",
    "oldlace",
    "red",
    "fuchsia",
    "magenta",
    "deeppink",
    "orangered",
    "tomato",
    "hotpink",
    "coral",
    "darkorange",
    "lightsalmon",
    "orange",
    "lightpink",
    "pink",
    "gold",
    "peachpuff",
    "navajowhite",
    "moccasin",
    "bisque",
    "mistyrose",
    "blanchedalmond",
    "papayawhip",
    "lavenderblush",
    "seashell",
    "cornsilk",
    "lemonchiffon",
    "floralwhite",
    "snow",
    "yellow",
    "lightyellow",
    "ivory",
    "white",
)
VALID_COLORS_SET = set(VALID_COLORS)
DEFAULT_TURTLE_SHAPE: TurtleShape = "turtle"
VALID_TURTLE_SHAPES: tuple[TurtleShape, ...] = ("turtle", "circle")
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">
        <rect width="100%" height="100%" fill="{background_color}"/>
        {lines}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style=" stroke:none;fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" d="M 18.214844 0.632812 C 16.109375 1.800781 15.011719 4.074219 15.074219 7.132812 L 15.085938 7.652344 L 14.785156 7.496094 C 13.476562 6.824219 11.957031 6.671875 10.40625 7.066406 C 8.46875 7.550781 6.515625 9.15625 4.394531 11.992188 C 3.0625 13.777344 2.679688 14.636719 3.042969 15.027344 L 3.15625 15.152344 L 3.519531 15.152344 C 4.238281 15.152344 4.828125 14.886719 8.1875 13.039062 C 9.386719 12.378906 10.371094 11.839844 10.378906 11.839844 C 10.386719 11.839844 10.355469 11.929688 10.304688 12.035156 C 9.832031 13.09375 9.257812 14.820312 8.96875 16.078125 C 7.914062 20.652344 8.617188 24.53125 11.070312 27.660156 C 11.351562 28.015625 11.363281 27.914062 10.972656 28.382812 C 8.925781 30.84375 7.945312 33.28125 8.238281 35.1875 C 8.289062 35.527344 8.28125 35.523438 8.917969 35.523438 C 10.941406 35.523438 13.074219 34.207031 15.136719 31.6875 C 15.359375 31.417969 15.328125 31.425781 15.5625 31.574219 C 16.292969 32.042969 18.023438 32.964844 18.175781 32.964844 C 18.335938 32.964844 19.941406 32.210938 20.828125 31.71875 C 20.996094 31.625 21.136719 31.554688 21.136719 31.558594 C 21.203125 31.664062 21.898438 32.414062 22.222656 32.730469 C 23.835938 34.300781 25.5625 35.132812 27.582031 35.300781 C 27.90625 35.328125 27.9375 35.308594 28.007812 34.984375 C 28.382812 33.242188 27.625 30.925781 25.863281 28.425781 L 25.542969 27.96875 L 25.699219 27.785156 C 28.945312 23.960938 29.132812 18.699219 26.257812 11.96875 L 26.207031 11.84375 L 27.945312 12.703125 C 31.53125 14.476562 32.316406 14.800781 33.03125 14.800781 C 33.976562 14.800781 33.78125 13.9375 32.472656 12.292969 C 28.519531 7.355469 25.394531 5.925781 21.921875 7.472656 L 21.558594 7.636719 L 21.578125 7.542969 C 21.699219 6.992188 21.761719 5.742188 21.699219 5.164062 C 21.496094 3.296875 20.664062 1.964844 19.003906 0.855469 C 18.480469 0.503906 18.457031 0.5 18.214844 0.632812"/>
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """
      <g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
        <circle stroke="{turtle_color}" stroke-width="3" fill="transparent" r="12" cx="0" cy="0"/>
        <polygon points="0,19 3,16 -3,16" style="fill:{turtle_color};stroke:{turtle_color};stroke-width:2"/>
      </g>
    """


SPEED_TO_SEC_MAP = {
    1: 1.5,
    2: 0.9,
    3: 0.7,
    4: 0.5,
    5: 0.3,
    6: 0.18,
    7: 0.12,
    8: 0.06,
    9: 0.04,
    10: 0.02,
    11: 0.01,
    12: 0.001,
    13: 0.0001,
}


def _speedToSec(speed: int) -> float:
    """Helper function that maps [1,13] speed values to ms delays."""
    return SPEED_TO_SEC_MAP[speed]


turtle_speed = DEFAULT_SPEED

is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE
turtle_pos: tuple[int | float, int | float] = (
    DEFAULT_WINDOW_SIZE[0] // 2,
    DEFAULT_WINDOW_SIZE[1] // 2,
)
turtle_degree: int | float = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH
turtle_shape: TurtleShape = DEFAULT_TURTLE_SHAPE

drawing_window: DisplayHandle | None = None


def initializeTurtle(
    initial_speed: int = DEFAULT_SPEED,
    initial_window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE,
) -> None:
    """Construct the display for turtle."""
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
    global turtle_shape

    if not isinstance(initial_speed, int) or initial_speed not in range(1, 14):
        raise ValueError("initial_speed must be an integer in interval [1,13]")
    turtle_speed = initial_speed

    if not (
        isinstance(initial_window_size, tuple)
        and len(initial_window_size) == 2
        and isinstance(initial_window_size[0], int)
        and isinstance(initial_window_size[1], int)
    ):
        raise ValueError("window_size must be a tuple of 2 integers")

    window_size = initial_window_size

    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    pen_color = DEFAULT_PEN_COLOR
    turtle_pos = (window_size[0] // 2, window_size[1] // 2)
    turtle_degree = DEFAULT_TURTLE_DEGREE
    background_color = DEFAULT_BACKGROUND_COLOR
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH
    turtle_shape = DEFAULT_TURTLE_SHAPE

    drawing_window = display(HTML(_generateSvgDrawing()), display_id=True)


def _generateTurtleSvgDrawing() -> str:
    """Helper function for generating svg string of the turtle."""
    if is_turtle_visible:
        vis = "visible"
    else:
        vis = "hidden"

    turtle_x = turtle_pos[0]
    turtle_y = turtle_pos[1]
    degrees = turtle_degree
    template = ""

    if turtle_shape == "turtle":
        turtle_x -= 18
        turtle_y -= 18
        degrees += 90
        template = TURTLE_TURTLE_SVG_TEMPLATE
    else:  # circle
        degrees -= 90
        template = TURTLE_CIRCLE_SVG_TEMPLATE

    return template.format(
        turtle_color=pen_color,
        turtle_x=turtle_x,
        turtle_y=turtle_y,
        visibility=vis,
        degrees=degrees,
        rotation_x=turtle_pos[0],
        rotation_y=turtle_pos[1],
    )


def _generateSvgDrawing() -> str:
    """Helper function for generating the whole svg string."""
    return SVG_TEMPLATE.format(
        window_width=window_size[0],
        window_height=window_size[1],
        background_color=background_color,
        lines=svg_lines_string,
        turtle=_generateTurtleSvgDrawing(),
    )


def _updateDrawing() -> None:
    """Helper functions for updating the screen using the latest positions/angles/lines etc."""
    if drawing_window is None:
        raise AttributeError(
            "Display has not been initialized yet. Call initializeTurtle() before using."
        )
    time.sleep(_speedToSec(turtle_speed))
    drawing_window.update(HTML(_generateSvgDrawing()))


def _moveToNewPosition(new_pos: tuple[int | float, int | float]) -> None:
    """Helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down."""
    global turtle_pos
    global svg_lines_string

    # rounding the new_pos to eliminate floating point errors.
    new_pos = (round(new_pos[0], 3), round(new_pos[1], 3))

    start_pos = turtle_pos
    if is_pen_down:
        svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0],
            y1=start_pos[1],
            x2=new_pos[0],
            y2=new_pos[1],
            pen_color=pen_color,
            pen_width=pen_width,
        )

    turtle_pos = new_pos
    _updateDrawing()


def forward(units: int | float) -> None:
    """Makes the turtle move forward by 'units' units."""
    if not isinstance(units, (int, float)):
        raise ValueError("units must be a number.")

    alpha = math.radians(turtle_degree)
    ending_point = (
        turtle_pos[0] + units * math.cos(alpha),
        turtle_pos[1] + units * math.sin(alpha),
    )

    _moveToNewPosition(ending_point)


fd = forward  # alias


def backward(units: int | float) -> None:
    """Makes the turtle move backward by 'units' units."""
    if not isinstance(units, (int, float)):
        raise ValueError("units must be a number.")
    forward(-1 * units)


bk = backward  # alias
back = backward  # alias


def right(degrees: int | float) -> None:
    """Makes the turtle move right by 'degrees' degrees (NOT radians)."""
    global turtle_degree

    if not isinstance(degrees, (int, float)):
        raise ValueError("degrees must be a number.")

    turtle_degree = (turtle_degree + degrees) % 360
    _updateDrawing()


rt = right  # alias


def face(degrees: int | float) -> None:
    """Makes the turtle face a given direction."""
    global turtle_degree

    if not isinstance(degrees, (int, float)):
        raise ValueError("degrees must be a number.")

    turtle_degree = degrees % 360
    _updateDrawing()


setheading = face  # alias
seth = face  # alias


def left(degrees: int | float) -> None:
    """Makes the turtle move left by 'degrees' degrees (NOT radians, this library does not support radians right now)."""
    if not isinstance(degrees, (int, float)):
        raise ValueError("degrees must be a number.")
    right(-1 * degrees)


lt = left


def penup() -> None:
    """Raises the pen such that following turtle moves will not cause any drawings."""
    global is_pen_down

    is_pen_down = False
    # TODO: decide if we should put the timout after lifting the pen
    # _updateDrawing()


pu = penup  # alias
up = penup  # alias


def pendown() -> None:
    """Lowers the pen such that following turtle moves will now cause drawings."""
    global is_pen_down

    is_pen_down = True
    # TODO: decide if we should put the timout after releasing the pen
    # _updateDrawing()


pd = pendown  # alias
down = pendown  # alias


def isdown() -> bool:
    """Returns whether the pen is currently down."""
    return is_pen_down


@overload
def speed(speed: None = None) -> int: ...
@overload
def speed(speed: int) -> None: ...
def speed(speed: int | None = None) -> int | None:
    """Update the speed of the moves, [1,13].
    If argument is omitted, it returns the speed.
    """
    global turtle_speed

    if speed is None:
        return turtle_speed

    if not isinstance(speed, int) or speed not in range(1, 14):
        raise ValueError("speed must be an integer in the interval [1,13].")
    turtle_speed = speed
    # TODO: decide if we should put the timout after changing the speed
    # _updateDrawing()
    return None


def setx(x: int | float) -> None:
    """Move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same."""
    if not isinstance(x, (int, float)):
        raise ValueError("new x position must be a number.")
    if x < 0:
        raise ValueError("new x position must be non-negative.")
    _moveToNewPosition((x, turtle_pos[1]))


def sety(y: int | float) -> None:
    """Move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same."""
    if not isinstance(y, (int, float)):
        raise ValueError("new y position must be a number.")
    if y < 0:
        raise ValueError("new y position must be non-negative.")
    _moveToNewPosition((turtle_pos[0], y))


def home() -> None:
    """Takes the turtle to the beginning position and angle.
    The turtle will continue drawing during this operation if the pen is down.
    """
    global turtle_degree

    turtle_degree = DEFAULT_TURTLE_DEGREE
    _moveToNewPosition(
        (window_size[0] // 2, window_size[1] // 2)
    )  # this will handle updating the drawing.


def getx() -> int | float:
    """Retrieve the turtle's current 'x' x-coordinate."""
    return turtle_pos[0]


xcor = getx  # alias


def gety() -> int | float:
    """Retrieve the turtle's current 'y' y-coordinate."""
    return turtle_pos[1]


ycor = gety  # alias


def position() -> tuple[int | float, int | float]:
    """Retrieve the turtle's current position as a (x,y) tuple vector."""
    return turtle_pos


pos = position  # alias


def getheading() -> int | float:
    """Retrieve the turtle's current angle."""
    return turtle_degree


heading = getheading  # alias


@overload
def goto(x: tuple[int | float, int | float]) -> None: ...
@overload
def goto(x: int | float, y: int | float) -> None: ...
def goto(
    x: int | float | tuple[int | float, int | float], y: int | float | None = None
) -> None:
    """Move the turtle to a designated 'x'-'y' coordinate."""
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError("the tuple argument must be of length 2.")

        y = x[1]
        x = x[0]

    if not isinstance(x, (int, float)):
        raise ValueError("new x position must be a number.")
    if x < 0:
        raise ValueError("new x position must be non-negative")
    if not isinstance(y, (int, float)):
        raise ValueError("new y position must be a number.")
    if y < 0:
        raise ValueError("new y position must be non-negative.")
    _moveToNewPosition((x, y))


setpos = goto  # alias
setposition = goto  # alias


def showturtle() -> None:
    """Switch turtle visibility to ON."""
    global is_turtle_visible

    is_turtle_visible = True
    _updateDrawing()


st = showturtle  # alias


def hideturtle() -> None:
    """Switch turtle visibility to OFF."""
    global is_turtle_visible

    is_turtle_visible = False
    _updateDrawing()


ht = hideturtle  # alias


def isvisible() -> bool:
    """Returns whether turtle is currently visible."""
    return is_turtle_visible


def _validateColorString(color: str) -> bool:
    if color in VALID_COLORS_SET:  # 140 predefined html color names
        return True
    if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color):  # 3 or 6 digit hex color code
        return True
    v = r"(?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])"  # an integer in [0,255]
    if re.fullmatch(
        rf"rgb\(\s*(?:{v}\s*,\s*{v}\s*,\s*{v}|{v}\s+{v}\s+{v})\s*\)", color
    ):  # rgb color code, comma or space separated
        return True
    return False


def _validateColorTuple(color: tuple[object, ...]) -> bool:
    if len(color) != 3:
        return False
    if (
        not isinstance(color[0], int)
        or not isinstance(color[1], int)
        or not isinstance(color[2], int)
    ):
        return False
    if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
        return False
    return True


def _processColor(color: object) -> str:
    if isinstance(color, str):
        color = color.lower()
        if not _validateColorString(color):
            raise ValueError(
                "color is invalid. it can be a known html color name, 3-6 digit hex string or rgb string."
            )
        return color
    elif isinstance(color, tuple):
        if not _validateColorTuple(color):
            raise ValueError(
                "color tuple is invalid. it must be a tuple of three integers, which are in the interval [0,255]"
            )
        return "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
    else:
        raise ValueError("the first parameter must be a color string or a tuple")


@overload
def bgcolor(color: None = None, c2: None = None, c3: None = None) -> str: ...
@overload
def bgcolor(
    color: str | tuple[int, int, int], c2: None = None, c3: None = None
) -> None: ...
@overload
def bgcolor(color: int, c2: int, c3: int) -> None: ...
def bgcolor(
    color: str | tuple[int, int, int] | int | None = None,
    c2: int | None = None,
    c3: int | None = None,
) -> str | None:
    """Change the background color of the drawing area.
    If no params, return the current background color.
    """
    global background_color

    if color is None:
        return background_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError(
                "if the second argument is set, the third arguments must be set as well to complete the rgb set."
            )
        background_color = _processColor((color, c2, c3))
    else:
        background_color = _processColor(color)
    _updateDrawing()
    return None


@overload
def color(color: None = None, c2: None = None, c3: None = None) -> str: ...
@overload
def color(
    color: str | tuple[int, int, int], c2: None = None, c3: None = None
) -> None: ...
@overload
def color(color: int, c2: int, c3: int) -> None: ...
def color(
    color: str | tuple[int, int, int] | int | None = None,
    c2: int | None = None,
    c3: int | None = None,
) -> str | None:
    """Change the color of the pen.
    If no params, return the current pen color.
    """
    global pen_color

    if color is None:
        return pen_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError(
                "if the second argument is set, the third arguments must be set as well to complete the rgb set."
            )
        pen_color = _processColor((color, c2, c3))
    else:
        pen_color = _processColor(color)
    _updateDrawing()
    return None


pencolor = color


@overload
def width(width: None = None) -> int: ...
@overload
def width(width: int) -> None: ...
def width(width: int | None = None) -> int | None:
    """Change the width of the lines drawn by the turtle, in pixels.
    If the function is called without arguments, it returns the current width.
    """
    global pen_width

    if width is None:
        return pen_width
    else:
        if not isinstance(width, int):
            raise ValueError("new width position must be an integer.")
        if not width > 0:
            raise ValueError("new width position must be positive.")

        pen_width = width
        # TODO: decide if we should put the timout after changing the pen_width
        # _updateDrawing()
        return None


pensize = width


@overload
def distance(x: tuple[int | float, int | float]) -> float: ...
@overload
def distance(x: int | float, y: int | float) -> float: ...
def distance(
    x: int | float | tuple[int | float, int | float], y: int | float | None = None
) -> float:
    """Calculate the distance between the turtle and a given point."""
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError("the tuple argument must be of length 2.")

        y = x[1]
        x = x[0]

    if not isinstance(x, (int, float)):
        raise ValueError("given x position must be a number.")
    if x < 0:
        raise ValueError("given x position must be non-negative")
    if not isinstance(y, (int, float)):
        raise ValueError("given y position must be a number.")
    if y < 0:
        raise ValueError("given y position must be non-negative.")

    return round(math.sqrt((turtle_pos[0] - x) ** 2 + (turtle_pos[1] - y) ** 2), 4)


def clear() -> None:
    """Clear any text or drawing on the screen."""
    global svg_lines_string

    svg_lines_string = ""
    _updateDrawing()


def write(
    obj: object,
    *,
    align: TextAlign = "left",
    font: tuple[int, str, FontType] = (12, "Arial", "normal"),
    **kwargs: object,
) -> None:
    """Writes the string equivalent of any value to the screen.
    'align' and 'font' named parameters can be given as arguments optionally.
    """
    global svg_lines_string
    global turtle_pos
    text = str(obj)
    if align == "center":
        text_anchor = "middle"
    elif align == "right":
        text_anchor = "end"
    else:  # "left", and invalid values are silently treated as "left"
        text_anchor = "start"

    if (
        len(font) != 3
        or not isinstance(font[0], int)
        or not isinstance(font[1], str)
        or font[2] not in {"bold", "italic", "underline", "normal"}
    ):
        raise ValueError(
            "font parameter must be a triplet consisting of font size (int), font family (str) and font type. font type can be one of {bold, italic, underline, normal}"
        )
    font_size = font[0]
    font_family = font[1]
    font_type = font[2]

    style_string = ""
    style_string += "font-size:" + str(font_size) + "px;"
    style_string += "font-family:'" + font_family + "';"

    if font_type == "bold":
        style_string += "font-weight:bold;"
    elif font_type == "italic":
        style_string += "font-style:italic;"
    elif font_type == "underline":
        style_string += "text-decoration: underline;"

    svg_lines_string += """<text x="{x}" y="{y}" fill="{fill_color}" text-anchor="{align}" style="{style}">{text}</text>""".format(
        x=turtle_pos[0],
        y=turtle_pos[1],
        text=text,
        fill_color=pen_color,
        align=text_anchor,
        style=style_string,
    )

    _updateDrawing()


@overload
def shape(shape: None = None) -> TurtleShape: ...
@overload
def shape(shape: TurtleShape) -> None: ...
def shape(shape: TurtleShape | None = None) -> TurtleShape | None:
    """Takes a shape name and transforms the main character's look.
    If no argument is supplied, this function returns the name of the current shape.
    """
    global turtle_shape
    if shape is None:
        return turtle_shape
    elif shape not in VALID_TURTLE_SHAPES:
        raise ValueError(
            "shape is invalid. valid options are: " + str(VALID_TURTLE_SHAPES)
        )

    turtle_shape = shape
    _updateDrawing()
    return None


def window_width() -> int:
    """Return turtle window width."""
    return window_size[0]


def window_height() -> int:
    """Return turtle window height."""
    return window_size[1]
