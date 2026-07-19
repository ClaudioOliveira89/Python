from turtle import *
import colorsys as cs
import random
import math

# Tela
screen = Screen()
screen.setup(900, 900)
screen.bgcolor("black")
screen.title("Simulação visual - Buraco Negro")
screen.tracer(0)
screen.colormode(1.0)

# Tartarugas
fundo = Turtle()
fundo.hideturtle()
fundo.speed(0)

desenho = Turtle()
desenho.hideturtle()
desenho.speed(0)

# Estrelas fixas
estrelas = []

for _ in range(250):
    x = random.randint(-430, 430)
    y = random.randint(-430, 430)

    # Evita estrelas muito perto do buraco negro
    if math.sqrt(x**2 + y**2) > 140:
        tamanho = random.choice([1, 1, 1, 2, 2, 3])
        brilho = random.uniform(0.5, 1)
        estrelas.append((x, y, tamanho, brilho))

for x, y, tamanho, brilho in estrelas:
    fundo.penup()
    fundo.goto(x, y)
    fundo.dot(tamanho, (brilho, brilho, brilho))


# Partículas do disco de acreção
particulas = []

for _ in range(350):
    raio = random.uniform(100, 420)
    angulo = random.uniform(0, math.pi * 2)
    velocidade = random.uniform(0.015, 0.05)
    cor_base = random.uniform(0.02, 0.13)  # tons entre vermelho, laranja e amarelo
    tamanho = random.uniform(2, 5)

    particulas.append([raio, angulo, velocidade, cor_base, tamanho])


frame = 0


def desenhar_buraco_negro():
    # Sombra central
    desenho.penup()
    desenho.goto(0, 0)
    desenho.dot(170, "black")

    # Anel externo luminoso
    for raio, brilho in [(92, 0.9), (100, 0.6), (110, 0.35)]:
        desenho.penup()
        desenho.goto(0, -raio)
        desenho.pendown()
        desenho.pensize(2)
        desenho.pencolor(cs.hsv_to_rgb(0.08, 0.8, brilho))
        desenho.circle(raio)

    # Núcleo escuro final
    desenho.penup()
    desenho.goto(0, 0)
    desenho.dot(145, "black")


def animar():
    global frame

    desenho.clear()

    for p in particulas:
        raio, angulo, velocidade, cor_base, tamanho = p

        # Quanto mais perto do centro, mais rápido gira
        angulo += velocidade * (430 / raio)

        # Lentamente cai para dentro
        raio -= random.uniform(0.20, 0.55)

        # Quando cai no horizonte, renasce longe
        if raio < 82:
            raio = random.uniform(300, 430)
            angulo = random.uniform(0, math.pi * 2)

        p[0] = raio
        p[1] = angulo

        # Achatamento para parecer disco visto de lado
        x = math.cos(angulo) * raio
        y = math.sin(angulo) * raio * 0.38

        # Rastro curto
        x2 = math.cos(angulo - 0.08) * (raio + 4)
        y2 = math.sin(angulo - 0.08) * (raio + 4) * 0.38

        h = (cor_base + frame * 0.002) % 1
        cor = cs.hsv_to_rgb(h, 0.9, 1)

        desenho.penup()
        desenho.goto(x2, y2)
        desenho.pendown()
        desenho.pensize(tamanho)
        desenho.pencolor(cor)
        desenho.goto(x, y)

    desenhar_buraco_negro()

    screen.update()
    frame += 1
    screen.ontimer(animar, 20)


animar()
done()