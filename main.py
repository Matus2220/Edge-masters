import pygame
from Objekty import Auto, Prekazka, Stena

WIDTH, HEIGHT = 1280, 720
THICKNESS = 5

def loose(sock):
    print("Prehral si!")
    sock.close()
    pygame.quit()
    exit(0)

def win(sock):
    print("Vyhral si!")
    sock.close()
    pygame.quit()
    exit(0)

def run_game(sock, my_name: str, enemy_name: str, server_addr):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    my_car = Auto(screen, 100, 500, "yellow")
    enemy_car = Auto(screen, 100, 100, "red")  # zatiaľ statický protivník

    list_prekazok = [
        Prekazka(screen, 100, 50, "red", -1, 3),
        Prekazka(screen, 100, 150, "orange", -1, 2),
        Prekazka(screen, 100, 250, "blue", -1, 1)
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

        # pohyb iba môjho auta
        my_car.move(dx, dy)
        
        msg = f"POS;{my_name};{my_car.x};{my_car.y}"
        sock.sendto(msg.encode("utf-8"), server_addr)  # server_addr = (IP, port)

        # kolizia s prekazkami
        for prekazka in list_prekazok:
            if my_car.get_rect().colliderect(prekazka.get_rect()):
                loose(sock)

        # kolizia so stenami
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
