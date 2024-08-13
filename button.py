import pygame

class Button:

    def __init__(self, image, local_x, local_y, pressed_img=None):
        self.image = image
        self.unpressed = image
        self.pressed = pressed_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (local_x, local_y)
        self.clicked = False
            
    def draw(self, surface):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if self.pressed != None:
                self.image = self.pressed
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                         
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(pos) == False:
            self.image = self.unpressed
            
        surface.blit(self.image, (self.rect.x, self.rect.y))
