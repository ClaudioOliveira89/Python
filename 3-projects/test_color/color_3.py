from turtle import *
import colorsys as cs

speed(0)
pensize(2)
bgcolor("black")

h = 0

for i in range(300):
    c = cs.hsv_to_rgb(h, 1, 1)
    pencolor(c)

    circle(i)
    left(5)

    h += 0.006

done()


from turtle import *
import colorsys as cs

speed(0)
pensize(2)
bgcolor('black')
h = 0

for i in range(400):
    c = cs.hsv_to_rgb(h, 0.8, 1)
    pencolor(c)

    forward(i)
    left(59)

    h += 0.005

done()