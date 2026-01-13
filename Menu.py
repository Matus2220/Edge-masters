import threading
import socket
import time
from Client import run
from Server import run_server

def host_game():
    """Spustí server a potom klienta na localhost"""
    print("\n=== HOSTOVANIE HRY ===")
    
    # Získaj IP adresu pre zobrazenie
    host_ip = socket.gethostbyname(socket.gethostname())
    print(f"Tvoja IP adresa: {host_ip}")
    print("Daj túto IP adresu druhému hráčovi, aby sa mohol pripojiť.")
    print("Spúšťam server...\n")
    
    # Spustí server v samostatnom vlákne
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Počkaj chvíľu, aby sa server stihol spustiť
    print("Čakám 2 sekundy, kým sa server spustí...")
    time.sleep(2)
    
    # Spustí klienta na localhost ako host
    print("\nPripojujem sa ako prvý hráč (host)...")
    from Client import run
    run("127.0.0.1", is_hosting=True)

def join_game():
    """Pripojí sa na existujúci server"""
    print("\n=== PRIPOJENIE NA HRU ===")
    server_ip = input("Zadaj IP adresu servera: ").strip()
    if not server_ip:
        print("Chyba: IP adresa nemôže byť prázdna!")
        return
    from Client import run
    run(server_ip, is_hosting=False)

def main():
    print("=" * 50)
    print("   VITAJ V EDGE RUNNERS")
    print("=" * 50)
    print()
    print("1. Hostovať hru (spustí server a pripojí sa)")
    print("2. Pripojiť sa na hru")
    print("0. Koniec")
    print()
    
    while True:
        volba = input("Zadaj možnosť: ").strip()
        match volba:
            case "1":
                host_game()
                break
            case "2":
                join_game()
                break
            case "0":
                print("Dovidenia!")
                exit(0)
            case _:
                print("Neznáma možnosť, skús znova.")

if __name__ == "__main__":
    main()
