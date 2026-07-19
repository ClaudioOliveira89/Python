import pygame
import numpy as np
import math
import random

# Inicialização
pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação Interativa - Átomo estilo Game")

clock = pygame.time.Clock()

# Cores
BLACK = (5, 5, 15)
WHITE = (230, 230, 230)
GRAY = (90, 90, 110)
RED = (255, 70, 70)
BLUE = (80, 150, 255)
CYAN = (80, 255, 255)
YELLOW = (255, 220, 80)
GREEN = (80, 255, 120)

# Centro do átomo
center = np.array([WIDTH / 2, HEIGHT / 2], dtype=float)

# Configurações
speed_multiplier = 1.0
paused = False
show_trails = True

# Elétrons
electrons = []

for i in range(12):
    radius = random.choice([100, 160, 230, 300])
    angle = random.uniform(0, math.tau)
    speed = random.uniform(0.008, 0.025)
    size = random.randint(5, 8)

    electrons.append({
        "radius": radius,
        "angle": angle,
        "speed": speed,
        "size": size,
        "trail": []
    })


def draw_text(text, x, y, size=24, color=WHITE):
    font = pygame.font.SysFont("consolas", size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def reset_simulation():
    global electrons, speed_multiplier, paused

    speed_multiplier = 1.0
    paused = False

    for e in electrons:
        e["angle"] = random.uniform(0, math.tau)
        e["trail"].clear()


running = True

while running:
    clock.tick(60)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                reset_simulation()

            if event.key == pygame.K_t:
                show_trails = not show_trails

            if event.key == pygame.K_UP:
                speed_multiplier += 0.2

            if event.key == pygame.K_DOWN:
                speed_multiplier = max(0.2, speed_multiplier - 0.2)

    # Movimento do núcleo com mouse
    mouse_buttons = pygame.mouse.get_pressed()

    if mouse_buttons[0]:
        mouse_pos = pygame.mouse.get_pos()
        center = np.array(mouse_pos, dtype=float)

    # Fundo
    screen.fill(BLACK)

    # Órbitas
    for radius in [100, 160, 230, 300]:
        pygame.draw.circle(
            screen,
            GRAY,
            center.astype(int),
            radius,
            1
        )

    # Atualiza e desenha elétrons
    for e in electrons:
        if not paused:
            e["angle"] += e["speed"] * speed_multiplier

        x = center[0] + math.cos(e["angle"]) * e["radius"]
        y = center[1] + math.sin(e["angle"]) * e["radius"]

        pos = np.array([x, y], dtype=float)

        # Rastro
        e["trail"].append(pos.copy())

        if len(e["trail"]) > 35:
            e["trail"].pop(0)

        if show_trails and len(e["trail"]) > 2:
            for i in range(1, len(e["trail"])):
                alpha = i / len(e["trail"])
                color = (
                    int(CYAN[0] * alpha),
                    int(CYAN[1] * alpha),
                    int(CYAN[2] * alpha)
                )

                pygame.draw.line(
                    screen,
                    color,
                    e["trail"][i - 1].astype(int),
                    e["trail"][i].astype(int),
                    2
                )

        # Elétron
        pygame.draw.circle(
            screen,
            CYAN,
            pos.astype(int),
            e["size"]
        )

        # Brilho do elétron
        pygame.draw.circle(
            screen,
            (30, 120, 160),
            pos.astype(int),
            e["size"] + 5,
            1
        )

    # Núcleo
    nucleons = [
        (-25, -15, RED),
        (0, -25, BLUE),
        (25, -15, RED),
        (-15, 10, BLUE),
        (15, 10, RED),
        (0, 30, BLUE),
        (-35, 20, RED),
        (35, 20, BLUE),
    ]

    for dx, dy, color in nucleons:
        pygame.draw.circle(
            screen,
            color,
            (int(center[0] + dx), int(center[1] + dy)),
            20
        )

    # Brilho em volta do núcleo
    pygame.draw.circle(
        screen,
        YELLOW,
        center.astype(int),
        60,
        2
    )

    pygame.draw.circle(
        screen,
        (255, 180, 40),
        center.astype(int),
        75,
        1
    )

    # Interface
    draw_text("Simulacao visual de Atomo - estilo Game", 20, 20, 26, GREEN)
    draw_text("ESPACO: pausar | R: reset | T: rastro | Mouse esquerdo: mover nucleo", 20, 55, 18)
    draw_text("Seta CIMA/BAIXO: velocidade", 20, 80, 18)
    draw_text(f"Velocidade: {speed_multiplier:.1f}x", 20, 115, 20, YELLOW)
    draw_text(f"Pausado: {'Sim' if paused else 'Nao'}", 20, 140, 20, YELLOW)

    pygame.display.flip()

pygame.quit()