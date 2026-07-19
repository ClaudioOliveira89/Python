from turtle import *
import math
import colorsys as cs

screen = Screen()
screen.setup(900, 900)
screen.bgcolor("black")
screen.title("Simulação visual de um átomo")
screen.tracer(0)
screen.colormode(1.0)

nucleo = Turtle()
nucleo.hideturtle()
nucleo.speed(0)

eletron = Turtle()
eletron.hideturtle()
eletron.speed(0)

orbitas = Turtle()
orbitas.hideturtle()
orbitas.speed(0)

# Desenha as órbitas
orbitas.pensize(1)
orbitas.pencolor("gray")

for raio in [120, 200, 280]:
    orbitas.penup()
    orbitas.goto(0, -raio)
    orbitas.pendown()
    orbitas.circle(raio)

# Dados dos elétrons
eletrons = [
    {"raio": 120, "angulo": 0, "vel": 0.05, "tamanho": 12},
    {"raio": 120, "angulo": 3.14, "vel": 0.05, "tamanho": 12},
    {"raio": 200, "angulo": 1, "vel": 0.035, "tamanho": 10},
    {"raio": 200, "angulo": 4, "vel": 0.035, "tamanho": 10},
    {"raio": 280, "angulo": 2, "vel": 0.025, "tamanho": 8},
    {"raio": 280, "angulo": 5, "vel": 0.025, "tamanho": 8},
]

frame = 0


def desenhar_nucleo():
    nucleo.clear()

    # Prótons e nêutrons simbólicos
    particulas = [
        (-20, 15, "red"),
        (20, 15, "blue"),
        (-15, -20, "blue"),
        (15, -20, "red"),
        (0, 0, "red"),
        (0, 30, "blue"),
        (30, 0, "red"),
        (-30, 0, "blue"),
    ]

    for x, y, cor in particulas:
        nucleo.penup()
        nucleo.goto(x, y)
        nucleo.dot(35, cor)

    # Brilho em volta do núcleo
    nucleo.penup()
    nucleo.goto(0, 0)
    nucleo.dot(95, cs.hsv_to_rgb(0.08, 0.8, 0.25))


def animar():
    global frame

    eletron.clear()
    desenhar_nucleo()

    for e in eletrons:
        e["angulo"] += e["vel"]

        x = math.cos(e["angulo"]) * e["raio"]
        y = math.sin(e["angulo"]) * e["raio"]

        cor = cs.hsv_to_rgb((frame * 0.003) % 1, 0.8, 1)

        eletron.penup()
        eletron.goto(x, y)
        eletron.dot(e["tamanho"], cor)

    screen.update()
    frame += 1
    screen.ontimer(animar, 20)


animar()
done()