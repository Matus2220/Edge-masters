import pygame

class Auto:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 30, 15)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def get_rect(self):
        return self.rect

class Prekazka:
    def __init__(self, screen, x, y, color, direction=1, speed=3,):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 200, 80)

    def move_horizontal(self):
        # posun po osi X
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # ak vyjde mimo obrazovky → presun späť na opačnú stranu
        if self.x > 1280:         # mimo vpravo
            self.x = -50         # objaví sa vľavo
        elif self.x < -50:       # mimo vľavo
            self.x = 1280        # objaví sa vpravo

        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move_towards_player(self, speed):
        self.y += speed
        self.rect.y = self.y

    def get_rect(self):
        return self.rect




class Stena:
    def __init__(self, screen, x, y, width, height, color):
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move(self, speed):
        self.y += speed
        self.rect.y = self.y

    def get_rect(self):
        return self.rect


