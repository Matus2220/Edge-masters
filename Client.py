import socket, random
import threading
from main import run_game

serverIP = input("Zadaj IP servera: ")
server = (str(serverIP), 5678)

host = "0.0.0.0"              # ← presne takto
port = random.randint(6000, 10000)

print(f"Klient je poskytovany na IP -> {socket.gethostbyname(socket.gethostname())}")
print(f"Klient bezi na porte {port}")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

name = input("Zadaj svoj nick: ")

# event – čakanie na START od servera
start_event = threading.Event()

# globálna pozícia súpera, ktorú bude čítať run_game
enemy_pos = {"x": 100, "y": 100}  # default

def recive(sock):
    global enemy_pos
    while True:
        try:
            data, address = sock.recvfrom(1024)
            msg = data.decode('utf-8')
            print("DEBUG: prisla sprava:", repr(msg)) 

            if msg == "START":
                print("Protivnik je pripojeny, spustam hru!")
                start_event.set()
                
            if msg == "END":
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
        except:
            break

# spusti prijímacie vlákno
threading.Thread(target=recive, args=(s,), daemon=True).start()

# pošli úvodnú správu, aby ťa server zaregistroval
s.sendto(f"{name} sa pripojil.".encode('utf-8'), server)
print("Cakam na protivnika...")

# počkaj na START
start_event.wait()

# spusti hru – odovzdáme socket, svoje meno, meno súpera a server adresu + referenciu na enemy_pos
from functools import partial
print("DEBUG: event je set, spustam run_game")  # <--- pridaj
run_game(s, name, "enemy", server, enemy_pos)
s.close()
