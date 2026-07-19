from turtle import *
import colorsys as cs

speed(0)
pensize(2)
bgcolor("black")

h = 0

for i in range(360):
    c = cs.hsv_to_rgb(h, 0.9, 1)
    pencolor(c)

    circle(100)
    left(10)

    h += 0.01

done()