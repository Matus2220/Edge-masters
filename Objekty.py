import pygame

class Auto:
    def __init__(self, screen, x, y, color, img_path=None):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        
        # Načítaj obrázok ak je zadaný, inak použij rect
        if img_path:
            self.img = pygame.image.load(img_path)
            # Získaj veľkosť obrázka pre rect
            self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        else:
            self.img = None
            self.rect = pygame.Rect(self.x, self.y, 60, 30)

    def draw(self):
        if self.img:
            self.screen.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def get_rect(self):
        return self.rect

class Prekazka:
    def __init__(self, screen, x, y, color, direction, speed, line, obstacle_id=None):
        self.line = line
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.obstacle_id = obstacle_id  # Unikátne ID pre synchronizáciu
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
    
    def get_type(self):
        """Vráti typ prekážky pre serializáciu"""
        return "unknown"  # Override v podtriedach


class Mala_prekazka(Prekazka):
    def __init__(self, screen, x, y, color, direction, speed, line, img, obstacle_id=None):
        super().__init__(screen, x, y, color, direction, speed, line, obstacle_id)
        self.rect = pygame.Rect(self.x, self.y, 70, 35)
        self.img = img
    
    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
    
    def get_type(self):
        return "small"
        
        
class Stredna_prekazka(Prekazka):
    def __init__(self, screen, x, y, color, direction, speed, line, img, obstacle_id=None):
        super().__init__(screen, x, y, color, direction, speed, line, obstacle_id)
        self.rect = pygame.Rect(self.x, self.y, 80, 50)
        self.img = img
        
    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
    
    def get_type(self):
        return "normal"
        
        
class Velka_prekazka(Prekazka):
    def __init__(self, screen, x, y, color, direction, speed, line, img, obstacle_id=None):
        super().__init__(screen, x, y, color, direction, speed, line, obstacle_id)
        self.rect = pygame.Rect(self.x, self.y, 200, 60)
        self.img = img
        
    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
    
    def get_type(self):
        return "large"


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


