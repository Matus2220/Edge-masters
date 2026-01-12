from Client import run

print("--- VYTAJ V EDGE RUNNERS ---")
print("------- zvol moznost -------")
print("")
print("1. Zacni hru a cakaj na supera...")
print("0. Koniec...")

while True:
    volba = input("Zadaj moznost: ")
    match volba:
        case "1":
            run()
        case "0":
            exit(0)
        case _:
            print("Neznama volba")
