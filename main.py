import pygame
from Objekty import Auto, Prekazka, Stena

pygame.init()
screen = pygame.display.set_mode((1280, 720))
auto1 = Auto(screen, 10, 10, "yellow")
prekazka_test = Prekazka(screen, 100, 100, "red")
clock = pygame.time.Clock()
running = True
list_prekazok = []
list_prekazok.append(Prekazka(screen, 100, 100, "red", 1))
list_prekazok.append(Prekazka(screen, 300, 250, "orange", -1))
list_stien = []
list_stien.append(Stena(screen, 500, 500, "green"))

n = 88

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dx, dy = 0, 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        dy -= 4
    if keys[pygame.K_s]:
        dy += 4
    if keys[pygame.K_a]:
        dx -= 4
    if keys[pygame.K_d]:
        dx += 4

    # posun prekážok
    for prekazka in list_prekazok:
        prekazka.move_horizontal()

    # 1) najprv posuň auto
    auto1.move(dx, dy)

    # 2) kolízia s prekážkami – koniec hry
    for prekazka in list_prekazok:
        if auto1.get_rect().colliderect(prekazka.get_rect()):
            print("Kolizia s prekazkou!")
            running = False

    # 3) kolízia so stenami – vráť sa späť
    for stena in list_stien:
        if auto1.get_rect().colliderect(stena.get_rect()):
            print("Kolizia so stenou!")
            # vráť posledný pohyb
            auto1.move(-dx, -dy)

    # vykreslenie
    screen.fill((0, 0, 0))
    auto1.draw()
    for prekazka in list_prekazok:
        prekazka.draw()
    for stena in list_stien:
        stena.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
