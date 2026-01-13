import pygame
import random
import time
from Objekty import Auto, Mala_prekazka, Stredna_prekazka, Velka_prekazka, Stena

WIDTH, HEIGHT = 1280, 720
THICKNESS = 5



def loose(sock, my_name: str, server_addr):
    """Oznámi serveru, že hráč prehral"""
    try:
        msg = f"LOOSE;{my_name}"
        sock.sendto(msg.encode("utf-8"), server_addr)
    except:
        pass  # Ignorujeme chyby pri odosielaní

def run_game(sock, my_name: str, enemy_name: str, server_addr, enemy_pos_dict, obstacles_dict=None, is_host=False, game_result_dict=None):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load("cesta.png")
    clock = pygame.time.Clock()
    running = True
    
    # Premenné pre ukončenie hry
    if game_result_dict is None:
        game_result_dict = {"game_over": False, "result": None}
    game_over = False
    game_result = None  # "win" alebo "lose"
    
    if obstacles_dict is None:
        obstacles_dict = {}
    
    # Každý hráč vidí seba hore a súpera dole
    my_car = Auto(screen, 10, 250, "green", "MotorkaHrac.png")  # Hráč je vždy hore
    enemy_car = Auto(screen, enemy_pos_dict.get("x", 10), 450, "red", "MotorkaOpp.png")  # Súper je vždy dole
    
    random_zoznam = ["small", "normal", "large"]
    pozicie_prekazok = {
        "small": {
            "x": 1290,
            "lines-y": [85, 165, 250],
            "speed": 18,  # 1.5x rýchlejšie (12 * 1.5)
            "img": pygame.image.load("autoR.png"),
        },
        "normal": {
            "x": 1290,
            "lines-y": [75, 155, 240],
            "speed": 12,  # 1.5x rýchlejšie (8 * 1.5)
            "img": pygame.image.load("autoM.png"),
        },
        "large": {
            "x": 1290,
            "lines-y": [70, 150, 240],
            "speed": 6,  # 1.5x rýchlejšie (4 * 1.5)
            "img": pygame.image.load("autoH.png"),
        }
    }
    
    # Dictionary pre mapovanie ID -> objekt prekážky
    obstacles_by_id = {}
    obstacle_id_counter = 0
    
    # Počiatočné prekážky - len host ich vytvára a posiela
    list_prekazok = []
    if is_host:
        obs_id1 = str(obstacle_id_counter)
        obstacle_id_counter += 1
        obs1 = Stredna_prekazka(screen, 1290, 75, "blue", -1, 12, 1, pygame.image.load("autoM.png"), obs_id1)
        list_prekazok.append(obs1)
        obstacles_by_id[obs_id1] = obs1
        obstacles_dict[obs_id1] = {"type": "normal", "x": 1290, "y": 75, "line": 1, "speed": 12}
        
        obs_id2 = str(obstacle_id_counter)
        obstacle_id_counter += 1
        obs2 = Velka_prekazka(screen, 1290, 240, "red", -1, 6, 3, pygame.image.load("autoH.png"), obs_id2)
        list_prekazok.append(obs2)
        obstacles_by_id[obs_id2] = obs2
        obstacles_dict[obs_id2] = {"type": "large", "x": 1290, "y": 240, "line": 3, "speed": 6}
        
        # Pošli počiatočné prekážky klientovi
        for obs_id, obs_data in obstacles_dict.items():
            msg = f"OBSTACLE;CREATE;{obs_id};{obs_data['type']};{obs_data['x']};{obs_data['y']};{obs_data['line']};{obs_data['speed']}"
            if sock != None:
                sock.sendto(msg.encode("utf-8"), server_addr)
        
        line1 = False
        line2 = True
        line3 = False
    else:
        line1 = False
        line2 = False
        line3 = False

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

        # VYTVORENIE NOVÝCH PREKÁŽOK - len host vytvára a posiela, klient prijíma
        if is_host:
            # HOST: Vytváranie nových prekážok
            if line1:
                random_choice = random.choice(random_zoznam)
                # Kontrola počtu prekážok
                count_small = sum(1 for p in list_prekazok if isinstance(p, Mala_prekazka))
                count_normal = sum(1 for p in list_prekazok if isinstance(p, Stredna_prekazka))
                count_large = sum(1 for p in list_prekazok if isinstance(p, Velka_prekazka))
                
                while (count_small >= 2 and random_choice == "small") or \
                      (count_normal >= 2 and random_choice == "normal") or \
                      (count_large >= 2 and random_choice == "large"):
                    random_choice = random.choice(random_zoznam)
                
                x_prekazka = pozicie_prekazok[random_choice]
                obs_id = str(obstacle_id_counter)
                obstacle_id_counter += 1
                
                match random_choice:
                    case "small":
                        nahodna_prekazka = Mala_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][0], "yellow", -1, x_prekazka["speed"], 1, x_prekazka["img"], obs_id)
                    case "normal":
                        nahodna_prekazka = Stredna_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][0], "blue", -1, x_prekazka["speed"], 1, x_prekazka["img"], obs_id)
                    case "large":
                        nahodna_prekazka = Velka_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][0], "red", -1, x_prekazka["speed"], 1, x_prekazka["img"], obs_id)
                
                list_prekazok.append(nahodna_prekazka)
                obstacles_by_id[obs_id] = nahodna_prekazka
                obstacles_dict[obs_id] = {"type": random_choice, "x": x_prekazka["x"], "y": x_prekazka["lines-y"][0], "line": 1, "speed": x_prekazka["speed"]}
                
                # Pošli CREATE správu
                msg = f"OBSTACLE;CREATE;{obs_id};{random_choice};{x_prekazka['x']};{x_prekazka['lines-y'][0]};1;{x_prekazka['speed']}"
                if sock != None:
                    sock.sendto(msg.encode("utf-8"), server_addr)
                line1 = False
                
            if line2:
                random_choice = random.choice(random_zoznam)
                count_small = sum(1 for p in list_prekazok if isinstance(p, Mala_prekazka))
                count_normal = sum(1 for p in list_prekazok if isinstance(p, Stredna_prekazka))
                count_large = sum(1 for p in list_prekazok if isinstance(p, Velka_prekazka))
                
                while (count_small >= 2 and random_choice == "small") or \
                      (count_normal >= 2 and random_choice == "normal") or \
                      (count_large >= 2 and random_choice == "large"):
                    random_choice = random.choice(random_zoznam)
                
                x_prekazka = pozicie_prekazok[random_choice]
                obs_id = str(obstacle_id_counter)
                obstacle_id_counter += 1
                
                match random_choice:
                    case "small":
                        nahodna_prekazka = Mala_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][1], "yellow", -1, x_prekazka["speed"], 2, x_prekazka["img"], obs_id)
                    case "normal":
                        nahodna_prekazka = Stredna_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][1], "blue", -1, x_prekazka["speed"], 2, x_prekazka["img"], obs_id)
                    case "large":
                        nahodna_prekazka = Velka_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][1], "red", -1, x_prekazka["speed"], 2, x_prekazka["img"], obs_id)
                
                list_prekazok.append(nahodna_prekazka)
                obstacles_by_id[obs_id] = nahodna_prekazka
                obstacles_dict[obs_id] = {"type": random_choice, "x": x_prekazka["x"], "y": x_prekazka["lines-y"][1], "line": 2, "speed": x_prekazka["speed"]}
                
                # Pošli CREATE správu
                msg = f"OBSTACLE;CREATE;{obs_id};{random_choice};{x_prekazka['x']};{x_prekazka['lines-y'][1]};2;{x_prekazka['speed']}"
                if sock != None:
                    sock.sendto(msg.encode("utf-8"), server_addr)
                line2 = False
                
            if line3:
                random_choice = random.choice(random_zoznam)
                count_small = sum(1 for p in list_prekazok if isinstance(p, Mala_prekazka))
                count_normal = sum(1 for p in list_prekazok if isinstance(p, Stredna_prekazka))
                count_large = sum(1 for p in list_prekazok if isinstance(p, Velka_prekazka))
                
                while (count_small >= 2 and random_choice == "small") or \
                      (count_normal >= 2 and random_choice == "normal") or \
                      (count_large >= 2 and random_choice == "large"):
                    random_choice = random.choice(random_zoznam)
                
                x_prekazka = pozicie_prekazok[random_choice]
                obs_id = str(obstacle_id_counter)
                obstacle_id_counter += 1
                
                match random_choice:
                    case "small":
                        nahodna_prekazka = Mala_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][2], "yellow", -1, x_prekazka["speed"], 3, x_prekazka["img"], obs_id)
                    case "normal":
                        nahodna_prekazka = Stredna_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][2], "blue", -1, x_prekazka["speed"], 3, x_prekazka["img"], obs_id)
                    case "large":
                        nahodna_prekazka = Velka_prekazka(screen, x_prekazka["x"], x_prekazka["lines-y"][2], "red", -1, x_prekazka["speed"], 3, x_prekazka["img"], obs_id)
                
                list_prekazok.append(nahodna_prekazka)
                obstacles_by_id[obs_id] = nahodna_prekazka
                obstacles_dict[obs_id] = {"type": random_choice, "x": x_prekazka["x"], "y": x_prekazka["lines-y"][2], "line": 3, "speed": x_prekazka["speed"]}
                
                # Pošli CREATE správu
                msg = f"OBSTACLE;CREATE;{obs_id};{random_choice};{x_prekazka['x']};{x_prekazka['lines-y'][2]};3;{x_prekazka['speed']}"
                if sock != None:
                    sock.sendto(msg.encode("utf-8"), server_addr)
                line3 = False

            # HOST: Pohyb prekážok a odosielanie pozícií
            for prekazka in list_prekazok[:]:  # Kópia zoznamu pre bezpečné odstraňovanie
                move_result = prekazka.move_horizontal()
                if move_result[0] == False:
                    # Prekážka vyšla z obrazovky
                    obs_id = prekazka.obstacle_id
                    list_prekazok.remove(prekazka)
                    if obs_id in obstacles_by_id:
                        del obstacles_by_id[obs_id]
                    if obs_id in obstacles_dict:
                        del obstacles_dict[obs_id]
                    
                    # Pošli REMOVE správu
                    msg = f"OBSTACLE;REMOVE;{obs_id}"
                    if sock != None:
                        sock.sendto(msg.encode("utf-8"), server_addr)
                    
                    # Aktivuj príslušnú linku
                    match move_result[1]:
                        case 1:
                            line1 = True
                        case 2:
                            line2 = True
                        case 3:
                            line3 = True
                else:
                    # Pošli pozíciu prekážky
                    obs_id = prekazka.obstacle_id
                    if obs_id:
                        msg = f"OBSTACLE;POS;{obs_id};{prekazka.x};{prekazka.y}"
                        if sock != None:
                            sock.sendto(msg.encode("utf-8"), server_addr)
        
        else:
            # KLIENT: Aktualizácia prekážok z obstacles_dict
            # Vytvor/aktualizuj prekážky podľa obstacles_dict
            for obs_id, obs_data in obstacles_dict.items():
                if obs_id not in obstacles_by_id:
                    # Vytvor novú prekážku
                    obs_type = obs_data["type"]
                    x = obs_data["x"]
                    y = obs_data["y"]  # Rovnaká pozícia ako u hosta
                    line = obs_data["line"]
                    speed = obs_data["speed"]
                    
                    match obs_type:
                        case "small":
                            new_obs = Mala_prekazka(screen, x, y, "yellow", -1, speed, line, pozicie_prekazok["small"]["img"], obs_id)
                        case "normal":
                            new_obs = Stredna_prekazka(screen, x, y, "blue", -1, speed, line, pozicie_prekazok["normal"]["img"], obs_id)
                        case "large":
                            new_obs = Velka_prekazka(screen, x, y, "red", -1, speed, line, pozicie_prekazok["large"]["img"], obs_id)
                        case _:
                            continue
                    
                    list_prekazok.append(new_obs)
                    obstacles_by_id[obs_id] = new_obs
                else:
                    # Aktualizuj pozíciu existujúcej prekážky
                    obstacles_by_id[obs_id].x = obs_data["x"]
                    obstacles_by_id[obs_id].y = obs_data["y"]  # Rovnaká pozícia
                    obstacles_by_id[obs_id].rect.x = obs_data["x"]
                    obstacles_by_id[obs_id].rect.y = obs_data["y"]
            
            # Odstráň prekážky, ktoré už nie sú v obstacles_dict
            for obs_id in list(obstacles_by_id.keys()):
                if obs_id not in obstacles_dict:
                    if obstacles_by_id[obs_id] in list_prekazok:
                        list_prekazok.remove(obstacles_by_id[obs_id])
                    del obstacles_by_id[obs_id]

        # pohyb môjho auta
        my_car.move(dx, dy)

        # POS správa na server
        msg = f"POS;{my_name};{my_car.x};{my_car.y}"
        if sock != None:
            sock.sendto(msg.encode("utf-8"), server_addr)

        # aktualizácia pozície súpera z enemy_pos_dict
        # Každý hráč vidí súpera vždy dole (y=450)
        # Pozícia X sa berie z enemy_pos_dict, Y je vždy 450 (dole)
        enemy_car.x = enemy_pos_dict.get("x", 10)
        enemy_car.y = 450  # Súper je vždy dole
        enemy_car.rect.x = enemy_car.x
        enemy_car.rect.y = enemy_car.y

        # Skontroluj výsledok hry z game_result_dict (ak súper prehral, tento hráč vyhral)
        # Táto kontrola sa musí dejať v každom cykle, aby sa zachytila zmena z receive() vlákna
        if game_result_dict.get("game_over", False) and not game_over:
            game_over = True
            game_result = game_result_dict.get("result", None)
            # Ak súper prehral, tento hráč vyhral
            if game_result == "win":
                print("\n ------------------------------------------------ \n VYHRAL SI! \n------------------------------------------------ \n")
        
        # kolízia s prekážkami
        if not game_over:
            for prekazka in list_prekazok:
                if my_car.get_rect().colliderect(prekazka.get_rect()):
                    # Hráč prehral
                    game_over = True
                    game_result = "lose"
                    game_result_dict["game_over"] = True
                    game_result_dict["result"] = "lose"
                    loose(sock, my_name, server_addr)
                    break

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
        
        # Zobrazenie výsledku hry
        if game_over:
            # Vytvor veľký font pre výsledok
            font = pygame.font.Font(None, 96)
            if game_result == "lose":
                text = font.render("PREHRAL SI!", True, (255, 0, 0))
            elif game_result == "win":
                text = font.render("VYHRAL SI!", True, (0, 255, 0))
            else:
                text = font.render("HRA SKONCILA", True, (255, 255, 0))
            
            # Zobraz text v strede obrazovky
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            # Počkaj 3 sekundy pred ukončením
            time.sleep(3)
            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
