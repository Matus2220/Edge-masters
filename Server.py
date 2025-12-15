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
    data, address = s.recvfrom(1024)
    clients.add(address)

    if len(clients) >= 2 and not game_started:
        print("Mame dvoch hracov, posielam START")
        for c in clients:
            s.sendto("START".encode("utf-8"), c)
        game_started = True

    msg = data.decode("utf-8")

    # ak je to pozícia, len ju prepošli súperovi, neprintuj
    if msg.startswith("POS;"):
        for c in clients:
            if c != address:
                s.sendto(data, c)
        continue

    # inak ide o „bežnú“ správu (chat, info...)
    print(f"Zadane udaje: {msg}")
    for c in clients:
        if c != address:
            s.sendto(data, c)
