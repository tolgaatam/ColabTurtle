Turtle for Google Colab notebooks
===================

Installation for Google Colab:
----
Create an empty code cell and type:

    !pip3 install ColabTurtle

Run the code cell.


Usage
----
In any code cell, import like following:

    from ColabTurtle.Turtle import *

As Colab stores the declared variables in the runtime, call this before using: 

    initializeTurtle()

Current API
----
This module's API is mostly close with the traditional turtle API. There are some differences, most notably, the angles are handled differently. 0 angle is east and the angles increase clockwise.


`forward(units) | fd(units)` -> Moves the turtle in the direction it is facing, by `units` pixels
`backward(units) | bk(units) | back(units)` -> Moves the turtle in the opposite of the direction it is facing, by `units` pixels

`right(degrees) | rt(degrees)` -> Turns the turtle to right by the given `degrees` many degrees.
`face(degrees) | heading(degrees) | setheading(degrees)` -> Turns the turtle to the direction given as `degrees`
`left(degrees) | lt(degrees)` -> Turns the turtle to left by the given `degrees` many degrees.

`penup() | pu() | up()` -> Lifts the pen, turtles movement will not draw anything after this function is called.
`pendown() | pd()` -> Puts the pen down, causing the turtle movements to start drawing again.

`speed(s)` -> Sets the speed of turtle's movements. `s` can be a value in interval [1,13] where 1 is the slowest and 13 is the fastest. If `s` is omitted, the function returns the current speed.

`setx(x)` -> Moves the turtle to the given `x` position, the y coordinate of the turtle stays the same.
`sety(y)` -> Moves the turtle to the given `y` position, the x coordinate of the turtle stays the same.

`home()` -> Takes the turtle to the beginning position and angle. The turtle will continue drawing during this operation if the pen is down.

`getx() | xcor()` -> Returns the current x coordinate of the turtle.
`gety() | ycor()` -> Returns the current y coordinate of the turtle.
`position() | pos()` -> Returns the current x,y coordinates of the turtle as a tuple.
`heading() | getheading()` -> Returns the direction that the turtle is looking at right now, in degrees.

&NewLine;
```
goto(x,y) | setpos(x,y) | setposition(x,y)` 
goto((x,y)) | setpos(x,y) | setposition(x,y)` 
```
Moves the turtle to the point defined by x,y. The coordinates can be given separately, or in a single tuple.

`showturtle() | st()` -> Makes the turtle visible.
`hideturtle() | ht()` -> Makes the turtle invisible.
`isvisible()` -> Returns whether turtle is currently visible as boolean.

&NewLine;
```
bgcolor()
bgcolor(color)
bgcolor(r,g,b)
```
If no parameter given, returns the current background color as string. Else, changes the background color of the drawing area. The color can be given as three separate color parameters as in the RGB color encoding: red,green,blue. The color can be given as a single string as well. Three different formats are accepted for this string:
- HTML standard color names: 140 color names defined as standard ( https://www.w3schools.com/colors/colors_names.asp ) . Examples: `"red"`, `"black"`, `"magenta"`, `"cyan"` etc.
- Hex string with 3 or 6 digits, like `"#fff"`, `"FFF"`, `"#dfdfdf"`, `"#DFDFDF"`
- RGB string, like `"rgb(10 20 30)"`, `"rgb(10, 20, 30)"`

&NewLine;
```
color() | pencolor()
color(color) | pencolor(color)
bgcolor(r,g,b) | pencolor(r,g,b)
```
The same as `bgcolor` but works with the turtle's pen's color.

`width(w) | pensize(w)` -> Changes the width of the pen. If the parameter is omitted, returns the current pen width.

&NewLine;
```
distance(x,y)
distance((x,y))
```
-> Returns the turtle's distance to a given point x,y. The coordinates can be given separately or as a single tuple.

`clear()` -> Clear any drawing on the screen.
`write(obj)` -> Supposed to write a text on the screen. NOT IMPLEMENTED YET. There is a placeholder function now that does not do anything.
`shape(s)` -> Supposed to update or return the shape of the turtle. NOT IMPLEMENTED YET. In this library, we only have the turtle as circle for now. There is a placeholder function that either returns `"circle"` if called without argument. If called with argument, it is a no-op.



HAVE FUN DRAWING!