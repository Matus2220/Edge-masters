import pygame
import random
from Objekty import Auto, Mala_prekazka, Stredna_prekazka, Velka_prekazka, Stena

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
    bg = pygame.image.load("cesta.png")
    clock = pygame.time.Clock()
    running = True
    line1 = False
    line2 = True
    line3 = False

    my_car = Auto(screen, 10, 250, "green")
    enemy_car = Auto(screen, enemy_pos_dict["x"], enemy_pos_dict["y"], "red")
    random_zoznam = ["small", "normal", "large"]
    pozicie_prekazok = {
        "small": {
            "x": 1290,
            "lines-y": [85, 165, 250],
            "speed": 12,
            "img": pygame.image.load("autoR.png"),
        },
        "normal": {
            "x": 1290,
            "lines-y": [75, 155, 240],
            "speed": 8,
            "img": pygame.image.load("autoM.png"),
        },
        "large": {
            "x": 1290,
            "lines-y": [70, 150, 240],
            "speed": 4,
            "img": pygame.image.load("autoH.png"),
        }
    }
    
    list_prekazok = [
        Stredna_prekazka(screen, 1290, 75, "blue", -1, 8, 1, pygame.image.load("autoM.png")),
        Velka_prekazka(screen, 1290, 240, "red", -1, 3, 3, pygame.image.load("autoH.png")),
    ]

    list_stien = [
        Stena(screen, 0, 50, WIDTH, THICKNESS, None),
        Stena(screen, 0, 315, WIDTH, THICKNESS, None),
        Stena(screen, 0, 405, WIDTH, THICKNESS, None),
        Stena(screen, 0, 665, WIDTH, THICKNESS, None),
        Stena(screen, 0, 0, 10, 720, None),
        Stena(screen, 1280, 0, 10, 720, None),
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy -= 9
        if keys[pygame.K_s]:
            dy += 9
        if keys[pygame.K_a]:
            dx -= 9
        if keys[pygame.K_d]:
            dx += 9
        if keys[pygame.K_UP]:
            dy -= 9
        if keys[pygame.K_DOWN]:
            dy += 9
        if keys[pygame.K_LEFT]:
            dx -= 9
        if keys[pygame.K_RIGHT]:
            dx += 9

        # VYTVORENIE NOVEJ PREKÁŽKY
        if line1:
            random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Mala_prekazka) == 2 and random_choice == "small":
                random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Stredna_prekazka) == 2 and random_choice == "normal":
                random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Velka_prekazka) == 2 and random_choice == "large":
                random_choice = random.choice(random_zoznam)
            x_prekazka = pozicie_prekazok[random_choice]
            match random_choice:
                case "small":
                    nahodna_prekazka = Mala_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][0], "yellow", -1, x_prekazka["speed"], 1, x_prekazka["img"])
                case "normal":
                    nahodna_prekazka = Stredna_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][0], "blue", -1, x_prekazka["speed"], 1, x_prekazka["img"])
                case "large":
                    nahodna_prekazka = Velka_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][0], "red", -1, x_prekazka["speed"], 1, x_prekazka["img"])
            list_prekazok.append(nahodna_prekazka)
            line1 = False
            
        if line2:
            random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Mala_prekazka) == 2 and random_choice == "small":
                random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Stredna_prekazka) == 2 and random_choice == "normal":
                random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Velka_prekazka) == 2 and random_choice == "large":
                random_choice = random.choice(random_zoznam)
            x_prekazka = pozicie_prekazok[random_choice]
            match random_choice:
                case "small":
                    nahodna_prekazka = Mala_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][1], "yellow", -1, x_prekazka["speed"], 2, x_prekazka["img"])
                case "normal":
                    nahodna_prekazka = Stredna_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][1], "blue", -1, x_prekazka["speed"], 2, x_prekazka["img"])
                case "large":
                    nahodna_prekazka = Velka_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][1], "red", -1, x_prekazka["speed"], 2, x_prekazka["img"])
            list_prekazok.append(nahodna_prekazka)
            line2 = False
            
        if line3:
            random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Mala_prekazka) == 2 and random_choice == "small":
                random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Stredna_prekazka) == 2 and random_choice == "normal":
                random_choice = random.choice(random_zoznam)
            while list_prekazok.count(Velka_prekazka) == 2 and random_choice == "large":
                random_choice = random.choice(random_zoznam) 
            x_prekazka = pozicie_prekazok[random_choice]
            match random_choice:
                case "small":
                    nahodna_prekazka = Mala_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][2], "yellow", -1, x_prekazka["speed"], 3, x_prekazka["img"])
                case "normal":
                    nahodna_prekazka = Stredna_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][2], "blue", -1, x_prekazka["speed"], 3, x_prekazka["img"])
                case "large":
                    nahodna_prekazka = Velka_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][2], "red", -1, x_prekazka["speed"], 3, x_prekazka["img"])
            list_prekazok.append(nahodna_prekazka)
            line3 = False

            
        for prekazka in list_prekazok:
            if prekazka.move_horizontal()[0] == False:
                list_prekazok.remove(prekazka)
                match (prekazka.move_horizontal()[1]):
                    case 1:
                        line1 = True
                    case 2:
                        line2 = True
                    case 3:
                        line3 = True
            else:
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
                pygame.quit()
                loose(sock, my_name, server_addr)
                exit(0)

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
