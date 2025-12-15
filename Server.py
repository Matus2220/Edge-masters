import socket

host = socket.gethostbyname(socket.gethostname())
print(f"Server je poskytovany na IP -> {str(host)}")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5678
s.bind((host, port))
clients = set()
print(f"Server bezi na porte {port}")

game_started = False

while True:
    try:
        data, address = s.recvfrom(1024)
    except ConnectionResetError:
        print("Klient sa odpojil (10054), server pokracuje dalej...")
        continue

    clients.add(address)
    msg = data.decode("utf-8")

    if len(clients) >= 2 and not game_started:
        print("Mame dvoch hracov, posielam START")
        for c in clients:
            s.sendto("START".encode("utf-8"), c)
        game_started = True

    if msg.startswith("POS;"):
        for c in list(clients):
            if c != address:
                try:
                    s.sendto(data, c)
                except ConnectionResetError:
                    print(f"Klient {c} sa odpojil pri POS, odstranujem ho.")
                    clients.discard(c)
        continue

    if msg.startswith("LOOSE;"):
        print("Hra skoncila, resetujem lobby.")
        for c in list(clients):
            try:
                s.sendto("END".encode("utf-8"), c)
            except ConnectionResetError:
                pass
        # reset lobby
        clients.clear()
        game_started = False
        continue

    print(f"Zadane udaje: {msg}")
    for c in list(clients):
        if c != address:
            try:
                s.sendto(data, c)
            except ConnectionResetError:
                print(f"Klient {c} sa odpojil, odstranujem ho.")
                clients.discard(c)
