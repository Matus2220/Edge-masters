import pygame

class Auto:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 60, 30)

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
    def __init__(self, screen, x, y, color, direction, speed, line,):
        self.line = line
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
        if self.x < -100:       # mimo vľavo
            return (False, self.line)        # zmaze sa
        else:
            return (True, self.line)

        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move_towards_player(self, speed):
        self.y += speed
        self.rect.y = self.y

    def get_rect(self):
        return self.rect


class Mala_prekazka(Prekazka):
    def __init__(self, screen, x, y, color, direction, speed, line, img):
        super().__init__(screen, x, y, color, direction, speed, line)
        self.rect = pygame.Rect(self.x, self.y, 70, 35)
        self.img = img
    
    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
        
        
class Stredna_prekazka(Prekazka):
    def __init__(self, screen, x, y, color, direction, speed, line, img):
        super().__init__(screen, x, y, color, direction, speed, line)
        self.rect = pygame.Rect(self.x, self.y, 80, 50)
        self.img = img
        
    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
        
        
class Velka_prekazka(Prekazka):
    def __init__(self, screen, x, y, color, direction, speed, line, img):
        super().__init__(screen, x, y, color, direction, speed, line)
        self.rect = pygame.Rect(self.x, self.y, 200, 60)
        self.img = img
        
    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))


class Stena:
    def __init__(self, screen, x, y, width, height, color=None):
        self.screen = screen
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        if self.color:
            pygame.draw.rect(self.screen, self.color, self.rect)
        
    def move(self, speed):
        self.y += speed
        self.rect.y = self.y

    def get_rect(self):
        return self.rect


