import socket
import random
import threading
from main import run_game

# GLOBÁLNE premenné
start_event = threading.Event()
name = ""

def run():
    global start_event, name
    
    serverIP = input("Zadaj IP servera: ")
    server = (str(serverIP), 5678)

    host = "0.0.0.0"
    port = random.randint(6000, 10000)

    print(f"Klient je poskytovany na IP -> {socket.gethostbyname(socket.gethostname())}")
    print(f"Klient bezi na porte {port}")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    global name
    name = input("Zadaj svoj nick: ")

    # globálna pozícia súpera
    enemy_pos = {"x": 10, "y": 10}

    # spusti prijímacie vlákno
    recv_thread = threading.Thread(target=receive, args=(s, enemy_pos), daemon=True)
    recv_thread.start()

    # pošli úvodnú správu
    s.sendto(f"{name} sa pripojil.".encode('utf-8'), server)
    print("Cakam na protivnika...")

    # počkaj na START
    start_event.wait()

    print("DEBUG: event je set, spustam run_game")
    run_game(s, name, "enemy", server, enemy_pos)
    s.close()

def receive(sock, enemy_pos):
    global name
    while True:
        try:
            data, address = sock.recvfrom(1024)
            msg = data.decode('utf-8')
            print("DEBUG: prisla sprava:", repr(msg))

            if msg == "START":
                print("Protivnik je pripojeny, spustam hru!")
                start_event.set()
                
            elif msg == "END":
                print("\n ------------------------------------------------ \n VYHRAL SI! \n------------------------------------------------ \n")
                sock.close()
                exit(0)

            elif msg.startswith("POS;"):
                # format: POS;meno;x;y
                parts = msg.split(";")
                if len(parts) == 4:
                    _, nick, x_str, y_str = parts
                    if nick != name:
                        enemy_pos["x"] = int(x_str)
                        enemy_pos["y"] = int(y_str)
                else:
                    print(msg)
            else:
                print(msg)
        except:
            break

