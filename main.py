import pygame
import random
from Objekty import Auto, Prekazka, Stena

WIDTH, HEIGHT = 1280, 720
THICKNESS = 5

def choose_car():
    pass

def loose(sock, my_name: str, server_addr):
    print("\n ------------------------------------------------ \n PREHRAL SI! \n------------------------------------------------ \n")
    msg = f"LOOSE;{my_name}"
    sock.sendto(msg.encode("utf-8"), server_addr)
    sock.close()
    pygame.quit()
    exit(0)

def run_game(sock, my_name: str, enemy_name: str, server_addr, enemy_pos_dict):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load("cesta.png")
    clock = pygame.time.Clock()
    running = True
    prev_prekazka = None

    my_car = Auto(screen, 10, 10, "yellow")
    enemy_car = Auto(screen, enemy_pos_dict["x"], enemy_pos_dict["y"], "red")

    sirky = {"small": 30, "normal": 50, "large": 90}
    list_prekazok = []  # definuj mimo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # NÁHODNÁ ZMENA PREKÁŽOK KAŽDÚ SEKUNDU
        if pygame.time.get_ticks() % 1000 < 16:  # ~1s (60fps)
            prekazka_typ = random.choice(["small", "normal", "large"])
            if prekazka_typ == prev_prekazka:
                prekazka_typ = random.choice(["small", "normal", "large"])
            prev_prekazka = prekazka_typ
            
            # VYTVOR NOVÉ PREKÁŽKY
            list_prekazok = [
                Prekazka(screen, 100, 50, "red", -1, 3),
                Prekazka(screen, 300, 150, "orange", -1, 2),
                Prekazka(screen, 500, 250, "blue", -1, 1),
                Prekazka(screen, 200, 450, "red", -1, 3),
                Prekazka(screen, 400, 550, "orange", -1, 2),
                Prekazka(screen, 600, 650, "blue", -1, 1)
            ]
            
            # NASTAV VEĽKOSŤ
            for p in list_prekazok:
                p.width = sirky[prekazka_typ]
                p.height = 60
                p.rect = pygame.Rect(p.x, p.y, p.width, p.height)

        list_stien = [
            Stena(screen, 0, 0, WIDTH, THICKNESS, None),
            Stena(screen, 0, 355, WIDTH, THICKNESS, None),
            Stena(screen, 0, HEIGHT - THICKNESS, WIDTH, THICKNESS, None),
        ]

        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy -= 4
        if keys[pygame.K_s]:
            dy += 4
        if keys[pygame.K_a]:
            dx -= 4
        if keys[pygame.K_d]:
            dx += 4

        for prekazka in list_prekazok:
            prekazka.move_horizontal()

        # pohyb môjho auta
        my_car.move(dx, dy)

        # POS správa na server
        msg = f"POS;{my_name};{my_car.x};{my_car.y}"
        if sock != None:
            sock.sendto(msg.encode("utf-8"), server_addr)

        # aktualizácia pozície súpera z enemy_pos_dict
        enemy_car.x = enemy_pos_dict["x"]
        enemy_car.y = enemy_pos_dict["y"]
        enemy_car.rect.x = enemy_car.x
        enemy_car.rect.y = enemy_car.y

        # kolízia s prekážkami
        for prekazka in list_prekazok:
            if my_car.get_rect().colliderect(prekazka.get_rect()):
                loose(sock, my_name, server_addr)

        # kolízia so stenami
        for stena in list_stien:
            if my_car.get_rect().colliderect(stena.get_rect()):
                my_car.move(-dx, -dy)

        screen.blit(bg, (0, 0))
        my_car.draw()
        enemy_car.draw()
        for prekazka in list_prekazok:
            prekazka.draw()
        for stena in list_stien:
            stena.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
