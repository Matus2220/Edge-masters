import socket
import random
import threading
from main import run_game

# GLOBÁLNE premenné
start_event = threading.Event()
name = ""
shutdown_flag = threading.Event()  # Flag pre ukončenie vlákien

def run(server_ip=None, is_hosting=False):
    global start_event, name, shutdown_flag
    
    # Reset eventov pre novú hru
    start_event.clear()
    shutdown_flag.clear()
    
    if server_ip is None:
        serverIP = input("Zadaj IP servera: ")
    else:
        serverIP = server_ip
    server = (str(serverIP), 5678)

    host = "0.0.0.0"
    port = random.randint(6000, 10000)

    print(f"Klient je poskytovany na IP -> {socket.gethostbyname(socket.gethostname())}")
    print(f"Klient bezi na porte {port}")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Nastav timeout, aby socket nečakal nekonečne
    s.settimeout(None)  # UDP socket môže mať timeout
    s.bind((host, port))
    
    name = input("Zadaj svoj nick: ")

    # globálna pozícia súpera
    enemy_pos = {"x": 10, "y": 10}
    
    # globálny dictionary pre prekážky (id -> {x, y, type, line, speed})
    obstacles_dict = {}
    
    # globálna premenná, či som host
    is_host = is_hosting

    # spusti prijímacie vlákno (NON-DAEMON, aby sa mohlo správne ukončiť)
    recv_thread = threading.Thread(target=receive, args=(s, enemy_pos, obstacles_dict), daemon=False)
    recv_thread.start()

    # pošli úvodnú správu
    try:
        s.sendto(f"{name} sa pripojil.".encode('utf-8'), server)
        print("Cakam na protivnika...")
    except Exception as e:
        print(f"Chyba pri pripojovaní na server: {e}")
        print("Skontroluj, či server beží a IP adresa je správna.")
        s.close()
        return

    # počkaj na START s timeoutom
    import time as time_module
    timeout_occurred = threading.Event()
    
    def timeout_handler():
        time_module.sleep(30)  # 30 sekúnd timeout
        if not start_event.is_set():
            timeout_occurred.set()
            print("\nTimeout: Server neodpovedá. Možno nie je dostupný alebo nie je pripojený druhý hráč.")
            print("Skús to znova.")
    
    timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
    timeout_thread.start()
    
    # Počkaj na START alebo timeout
    while not start_event.is_set() and not timeout_occurred.is_set():
        time_module.sleep(0.1)
    
    if timeout_occurred.is_set():
        s.close()
        return

    print("DEBUG: event je set, spustam run_game")
    try:
        run_game(s, name, "enemy", server, enemy_pos, obstacles_dict, is_host)
    finally:
        # Ukonči vlákno a zatvor socket
        shutdown_flag.set()
        try:
            s.close()
        except:
            pass
        # Počkaj na ukončenie vlákna (max 1 sekunda)
        recv_thread.join(timeout=1.0)

def receive(sock, enemy_pos, obstacles_dict):
    global name, is_host, shutdown_flag
    # Nastav timeout, aby sme mohli pravidelne kontrolovať shutdown_flag
    sock.settimeout(0.5)
    
    while not shutdown_flag.is_set():
        try:
            data, address = sock.recvfrom(1024)
            msg = data.decode('utf-8')
            print("DEBUG: prisla sprava:", repr(msg))

            if msg == "START":
                print("Protivnik je pripojeny, spustam hru!")
                start_event.set()
                
            elif msg == "END":
                print("\n ------------------------------------------------ \n VYHRAL SI! \n------------------------------------------------ \n")
                shutdown_flag.set()
                try:
                    sock.close()
                except:
                    pass
                return

            elif msg.startswith("POS;"):
                # format: POS;meno;x;y
                parts = msg.split(";")
                if len(parts) == 4:
                    _, nick, x_str, y_str = parts
                    if nick != name:
                        enemy_pos["x"] = int(x_str)
                        # Pozícia Y sa posiela tak, ako ju hráč má
                        # Host má y okolo 250 (hore), klient okolo 450 (dole)
                        # Keď host pošle y=250, klient to zobrazí na y=450 (otočené)
                        # Keď klient pošle y=450, host to zobrazí na y=250 (otočené)
                        enemy_pos["y"] = int(y_str)
                else:
                    print(msg)
            
            elif msg.startswith("OBSTACLE;"):
                # format: OBSTACLE;CREATE;id;type;x;y;line;speed alebo OBSTACLE;POS;id;x;y alebo OBSTACLE;REMOVE;id
                parts = msg.split(";")
                if len(parts) >= 3:
                    action = parts[1]
                    if action == "CREATE" and len(parts) == 8:
                        # OBSTACLE;CREATE;id;type;x;y;line;speed
                        obs_id = parts[2]
                        obs_type = parts[3]
                        obs_x = int(parts[4])
                        obs_y = int(parts[5])
                        obs_line = int(parts[6])
                        obs_speed = int(parts[7])
                        obstacles_dict[obs_id] = {
                            "type": obs_type,
                            "x": obs_x,
                            "y": obs_y,
                            "line": obs_line,
                            "speed": obs_speed
                        }
                    elif action == "POS" and len(parts) == 5:
                        # OBSTACLE;POS;id;x;y
                        obs_id = parts[2]
                        obs_x = int(parts[3])
                        obs_y = int(parts[4])
                        if obs_id in obstacles_dict:
                            obstacles_dict[obs_id]["x"] = obs_x
                            obstacles_dict[obs_id]["y"] = obs_y
                    elif action == "REMOVE" and len(parts) == 3:
                        # OBSTACLE;REMOVE;id
                        obs_id = parts[2]
                        if obs_id in obstacles_dict:
                            del obstacles_dict[obs_id]
            else:
                print(msg)
        except socket.timeout:
            # Timeout je OK, len kontrolujeme shutdown_flag
            continue
        except ConnectionResetError as e:
            # UDP socket môže mať tento problém, ale pokračujeme len ak nie je shutdown
            if not shutdown_flag.is_set():
                # Ticho ignorujeme, aby sme nevyrušovali hru
                pass
            continue
        except OSError as e:
            # Socket error - možno sa socket uzatvoril
            if shutdown_flag.is_set():
                # Ak sa ukončuje, len skončíme
                break
            if hasattr(e, 'winerror') and e.winerror == 10054:  # Windows error 10054
                # Ticho ignorujeme, aby sme nevyrušovali hru
                continue
            else:
                # Ak je socket uzatvorený, ukončíme
                if "Bad file descriptor" in str(e) or "Socket operation on non-socket" in str(e):
                    break
                continue
        except Exception as e:
            # Iné chyby - len ak nie je shutdown
            if not shutdown_flag.is_set():
                # Ticho ignorujeme, aby sme nevyrušovali hru
                pass
            continue

