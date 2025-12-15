import pygame
from Objekty import Auto, Prekazka, Stena

WIDTH, HEIGHT = 1280, 720
THICKNESS = 5

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
    clock = pygame.time.Clock()
    running = True

    my_car = Auto(screen, 100, 500, "yellow")
    enemy_car = Auto(screen, enemy_pos_dict["x"], enemy_pos_dict["y"], "red")

    list_prekazok = [
        #hore
        Prekazka(screen, 100, 50, "red", -1, 3),
        Prekazka(screen, 100, 150, "orange", -1, 2),
        Prekazka(screen, 100, 250, "blue", -1, 1),
        #dole
        Prekazka(screen, 100, 450, "red", -1, 3),
        Prekazka(screen, 100, 550, "orange", -1, 2),
        Prekazka(screen, 100, 650, "blue", -1, 1)
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        list_stien = [
            Stena(screen, 0, 0, WIDTH, THICKNESS, "green"),
            Stena(screen, 0, 355, WIDTH, THICKNESS, "green"),
            Stena(screen, 0, HEIGHT - THICKNESS, WIDTH, THICKNESS, "green"),
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

        screen.fill((0, 0, 0))
        my_car.draw()
        enemy_car.draw()
        for prekazka in list_prekazok:
            prekazka.draw()
        for stena in list_stien:
            stena.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
