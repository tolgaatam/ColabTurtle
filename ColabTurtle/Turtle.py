from IPython.display import display, Javascript, HTML
import time
import math

# Created at: 20th October 2018
#         by: Tolga Atam

# Class for drawing classic Turtle figures on Google Colab notebooks. 
# It uses html capabilites of IPython library to draw svg shapes inline.
# Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)
class ColabTurtle:
  
  def __init__(self, speed=4, window_size=(800,500)):
    self.speedToSecMap = {1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18, 7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02}
    
    if speed not in range(1,11):
      raise ValueError('speed should be an integer in interval [1,10]')
    self.timeout = self._speedToSec(speed)
    
    if not (isinstance(window_size, tuple) and len(window_size) == 2 and isinstance(window_size[0], int) and isinstance(window_size[1], int)):
      raise ValueError('window_size should be a tuple of 2 integers')
    self.window_size = window_size
    
    self.is_pen_down = True
    self.turtle_pos = (window_size[0]//2, window_size[1]//2)
    self.is_turtle_visible = True
    self.turtle_degree = 270
    self.svg_lines_string = ""
    self.background_color = 'black'
    self.pen_color = 'white'
    self.pen_width = 4
    
    
    self.valid_colors = ('white', 'yellow', 'orange', 'red', 'green', 'blue', 'purple', 'grey', 'black')
    
    self.svg_template = """
      <svg width="{window_width}" height="{window_height}">
        <rect width="100%" height="100%" fill="{background_color}"/>
        {lines}
        {turtle}
      </svg>
    """
    
    self.turtle_svg_template = """
      <g visibility={visibility} transform="rotate({degrees},{turtle_x},{turtle_y}) translate({turtle_x}, {turtle_y})">
        <circle stroke="{turtle_color}" stroke-width="3" fill="transparent" r="12" cx="0" cy="0"/>
        <polygon points="0,19 3,16 -3,16" style="fill:{turtle_color};stroke:{turtle_color};stroke-width:2"/>
      </g>
    """
    
    self.drawingWindow = display(HTML(self._genereateSvgDrawing()) , display_id=True)
  
  # helper function that maps [1,10] speed values to ms delays
  def _speedToSec(self, speed):
    return self.speedToSecMap[speed]
    
  # helper function for generating svg string of the turtle
  def _generateTurtleSvgDrawing(self):
    if self.is_turtle_visible:
      vis = 'visible'
    else:
      vis = 'hidden'
    
    return self.turtle_svg_template.format(turtle_color=self.pen_color, turtle_x = self.turtle_pos[0], turtle_y = self.turtle_pos[1], \
                                          visibility = vis, degrees = self.turtle_degree-90)

      
  # helper function for generating the whole svg string
  def _genereateSvgDrawing(self):
    return self.svg_template.format(window_width=self.window_size[0], window_height=self.window_size[1], background_color=self.background_color, lines=self.svg_lines_string, turtle=self._generateTurtleSvgDrawing())
  
  # helper functions for updating the screen using the latest positions/angles/lines etc.
  def _updateDrawing(self):
    time.sleep(self.timeout)
    self.drawingWindow.update(HTML(self._genereateSvgDrawing()))
  
  # makes the turtle move forward by 'units' units
  def forward(self, units):
    if not isinstance(units, int):
      raise ValueError('units should be an integer')
    
    alpha = math.radians(self.turtle_degree)
    ending_point = (self.turtle_pos[0] + units * math.cos(alpha), self.turtle_pos[1] + units * math.sin(alpha))
    
    self._moveToNewPosition(ending_point)
  
  # makes the turtle move backward by 'units' units
  def backward(self, units):
    if not isinstance(units, int):
      raise ValueError('units should be an integer')
    self.forward(-1 * units)
  
  # makes the turtle move right by 'degrees' degrees (NOT radians)
  def right(self, degrees):
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
      raise ValueError('degrees should be a number')
    
    self.turtle_degree = (self.turtle_degree + degrees) % 360
    self._updateDrawing()
  
  # makes the turtle move right by 'degrees' degrees (NOT radians)
  def left(self, degrees):
    if not (isinstance(degrees, int) or isinstance(degrees, float)):
      raise ValueError('degrees should be a number')   
    self.right(-1 * degrees)
  
  # raises the pen such that following turtle moves will not cause any drawings
  def penup(self):
    self.is_pen_down = False
    # TO-DO: decide if we should put the timout after lifting the pen
    #self._updateDrawing()
    
  # lowers the pen such that following turtle moves will now cause drawings
  def pendown(self):
    self.is_pen_down = True
    # TO-DO: decide if we should put the timout after releasing the pen
    #self._updateDrawing()
    
  # update the speed of the moves, [1,10]
  def speed(self, speed):
    if speed not in range(1,11):
      raise ValueError('speed should be an integer in the interval [1,10]')
    self.timeout = self._speedToSec(speed)
    # TO-DO: decide if we should put the timout after changing the speed
    #self._updateDrawing()
  
  # move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
  def setx(self, x):
    if not isinstance(x, int):
      raise ValueError('new x position should be an integer')
    if not x >= 0:
      raise ValueError('new x position should be nonnegative')
    self._moveToNewPosition((x, self.turtle_pos[1]))
  
  # move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
  def sety(self, y):
    if not isinstance(y, int):
      raise ValueError('new y position should be an integer')
    if not y >= 0:
      raise ValueError('new y position should be nonnegative')
    self._moveToNewPosition((self.turtle_pos[0], y)) 
    
  # move the turtle to a designated 'x'-'y' coordinate
  def goto(self, x, y):
    if not isinstance(x, int):
      raise ValueError('new x position should be an integer')
    if not x >= 0:
      raise ValueError('new x position should be nonnegative')
    if not isinstance(y, int):
      raise ValueError('new y position should be an integer')
    if not y >= 0:
      raise ValueError('new y position should be nonnegative')
    self._moveToNewPosition((x,y))
  
  # helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
  def _moveToNewPosition(self, new_pos):
    start_pos = self.turtle_pos
    if self.is_pen_down:
      self.svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(x1=start_pos[0], y1=start_pos[1], x2=new_pos[0], y2=new_pos[1], pen_color=self.pen_color, pen_width=self.pen_width)
    
    self.turtle_pos = new_pos
    self._updateDrawing()
  
  # switch turtle visibility to ON
  def showturtle(self):
    self.is_turtle_visible = True
    self._updateDrawing()
  
  # switch turtle visibility to ON
  def hideturtle(self):
    self.is_turtle_visible = False
    self._updateDrawing()
  
  # change the background color of the drawing area; valid colors are defined at self.valid_colors
  def bgcolor(self, color):
    if not color in self.valid_colors:
      raise ValueError('color value should be one of the following: ' + str(self.valid_colors))
    self.background_color = color
    self._updateDrawing()
  
  # change the color of the pen; valid colors are defined at self.valid_colors
  def color(self, color):
    if not color in self.valid_colors:
      raise ValueError('color value should be one of the following: ' + str(self.valid_colors))
    self.pen_color = color
    self._updateDrawing()
    
  # change the width of the lines drawn by the turtle, in pixels
  def width(self, width):
    if not isinstance(width, int):
      raise ValueError('new width position should be an integer')
    if not width > 0:
      raise ValueError('new width position should be positive')
      
    self.pen_width = width
    self._updateDrawing()
