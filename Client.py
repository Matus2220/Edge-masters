import socket, random
import threading
from main import run_game

def recive(sock):
    while True:
        try:
            data, address = sock.recvfrom(1024)
            msg = data.decode('utf-8')
            if msg == "START":
                print("Protivnik je pripojeny, spustam hru!")
                run_game(sock, name, msg.split(" ")[1], server)
            else:
                print(msg)
        except:
            break

serverIP = input("Zadaj IP servera: ")
server = (str(serverIP), 5678)

host = socket.gethostbyname(socket.gethostname())
port = random.randint(6000, 10000)

print(f"Klient je poskytovany na IP -> {str(host)}")
print(f"Klient bezi na porte {port}")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

threading.Thread(target=recive, args=(s,), daemon=True).start()

name = input("Zadaj svoj nick: ")

# pošli úvodnú správu, aby ťa server zaregistroval
s.sendto(f"{name} sa pripojil.".encode('utf-8'), server)

print("Cakam na protivnika...")

