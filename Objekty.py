import pygame

class Auto:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

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
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 50)  

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move_towards_player(self, speed):
        self.y += speed
        self.rect.y = self.y

    def get_rect(self):
        return self.rect


class Stena:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 50)  

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move(self, speed):
        self.y += speed
        self.rect.y = self.y

    def get_rect(self):
        return self.rect
