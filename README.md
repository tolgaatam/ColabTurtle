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

An example code is given in the end of this documentation. Scroll down for it.

Current API
----
This module's API is mostly close with the traditional turtle API. There are some differences, most notably: the angles are handled differently. 0 angle is east and the angles increase clockwise. Some functions from the traditional turtle library is missing here; however almost all the main functionality is implemented. The functions that this library implements are explained below:


`forward(units) | fd(units)` -> Moves the turtle in the direction it is facing, by `units` pixels

`backward(units) | bk(units) | back(units)` -> Moves the turtle in the opposite of the direction it is facing, by `units` pixels

<br/>

`right(degrees) | rt(degrees)` -> Turns the turtle to right by the given `degrees` many degrees.

`face(degrees) | heading(degrees) | setheading(degrees)` -> Turns the turtle to the direction given as `degrees`

`left(degrees) | lt(degrees)` -> Turns the turtle to left by the given `degrees` many degrees.

<br/>

`penup() | pu() | up()` -> Lifts the pen, turtles movement will not draw anything after this function is called.

`pendown() | pd()` -> Puts the pen down, causing the turtle movements to start drawing again.

<br/>

`speed(s)` -> Sets the speed of turtle's movements. `s` can be a value in interval [1,13] where 1 is the slowest and 13 is the fastest. If `s` is omitted, the function returns the current speed.

<br/>

`setx(x)` -> Moves the turtle to the given `x` position, the y coordinate of the turtle stays the same.

`sety(y)` -> Moves the turtle to the given `y` position, the x coordinate of the turtle stays the same.

`home()` -> Takes the turtle to the beginning position and angle. The turtle will continue drawing during this operation if the pen is down.

<br/>

`getx() | xcor()` -> Returns the current x coordinate of the turtle.

`gety() | ycor()` -> Returns the current y coordinate of the turtle.

`position() | pos()` -> Returns the current x,y coordinates of the turtle as a tuple.

`heading() | getheading()` -> Returns the direction that the turtle is looking at right now, in degrees.

<br/>

<br/>

```
goto(x,y) | setpos(x,y) | setposition(x,y)` 
goto((x,y)) | setpos(x,y) | setposition(x,y)` 
```
Moves the turtle to the point defined by x,y. The coordinates can be given separately, or in a single tuple.

<br/>

<br/>

`showturtle() | st()` -> Makes the turtle visible.

`hideturtle() | ht()` -> Makes the turtle invisible.

`isvisible()` -> Returns whether turtle is currently visible as boolean.

<br/>

<br/>

```
bgcolor()
bgcolor(color)
bgcolor(r,g,b)
```
If no parameter given, returns the current background color as string. Else, changes the background color of the drawing area. The color can be given as three separate color parameters as in the RGB color encoding: red,green,blue. The color can be given as a single string as well. Three different formats are accepted for this string:
- HTML standard color names: 140 color names defined as standard ( https://www.w3schools.com/colors/colors_names.asp ) . Examples: `"red"`, `"black"`, `"magenta"`, `"cyan"` etc.
- Hex string with 3 or 6 digits, like `"#fff"`, `"FFF"`, `"#dfdfdf"`, `"#DFDFDF"`
- RGB string, like `"rgb(10 20 30)"`, `"rgb(10, 20, 30)"`

<br/>

<br/>

```
color() | pencolor()
color(color) | pencolor(color)
bgcolor(r,g,b) | pencolor(r,g,b)
```
The same as `bgcolor` but works with the turtle's pen's color.

<br/>

<br/>

`width(w) | pensize(w)` -> Changes the width of the pen. If the parameter is omitted, returns the current pen width.

<br/>

<br/>

```
distance(x,y)
distance((x,y))
```
Returns the turtle's distance to a given point x,y. The coordinates can be given separately or as a single tuple.

<br/>

<br/>

`clear()` -> Clear any drawing on the screen.

`write(obj, align=, font=)` -> Writes the string equivalent of any value to the screen. `align` and `font` **named** parameters can be given as arguments optionally. `align` must be one of `"left","center","right"`. It specifies where to put the text with respect to the turtle. `font` must be a tuple of three values like `(20, "Arial", "bold")`. The first value is the size, second value is the font family (only the ones that your browser natively supports must be used), the third value is font style that must be one of `"normal","bold","italic","underline"`.

`shape(sh)` -> Takes a shape name `sh` and transforms the main character's look. This library only has `'circle'` and `'turtle'` shapes available. If no argument is supplied, this function returns the name of the current shape.

`window_width()` -> Return the width of the turtle window.

`window_height()` -> Return the height of the turtle window.


<br/>

Example
----

```
initializeTurtle()
color('mediumblue')
penup()
goto(100, 250)
pendown()
forward(100)
left(90)
forward(40)
right(180)
forward(80)
penup()
right(90)
forward(50)
left(90)
forward(50)
left(90)
backward(10)
pendown()
speed(10)
for i in range(18):
    forward(17)
    right(20)
penup()
shape('circle')
color(230, 90, 120)
speed(7)
right(90)
forward(160)
left(90)
forward(60)
right(180)
pendown()
forward(100)
left(90)
forward(80)
penup()
shape('turtle')
forward(50)
left(90)
forward(40)
pendown()
for i in range(5):
    forward(17)
    right(20)
left(200)
for i in range(13):
    forward(17)
    left(20)
left(90)
forward(50)
penup()
backward(100)
left(90)
forward(40)
pendown()
left(155)
forward(105)
right(130)
forward(105)
backward(45)
right(115)
forward(50)
bgcolor("#dfdfdf")
penup()
backward(70)
left(90)
forward(100)
right(90)
pencolor('black')
pensize(7)
pendown()
forward(650)
left(180)
speed(12)
for i in range(90):
    forward(7)
    right(0.2)
speed(2)
left(18+180)
penup()
forward(300)
right(90)
color('rgb(70 110 70)')
```

This code ends up with the following drawing:

![Drawing that reads "Tolga"](sample_image.jpg?raw=true "Example Code's Final Look")

<br/>

<br/>

<br/>

HAVE FUN DRAWING!
