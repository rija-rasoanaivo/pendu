import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 400))
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
background = GREY
screen.fill(background)

running = True
while True:
    for event in pygame.event.get():
        #partie corp
        pygame.draw.rect(screen, MAGENTA, (375, 50, 2, 50))#corde
        pygame.draw.ellipse(screen, RED, (350, 100, 50, 50), 1)#tête
        pygame.draw.rect(screen, RED, (375, 150, 1, 100))#corp
        pygame.draw.line(screen, RED, (375, 175), (340, 150), 1)#bras gauche
        pygame.draw.line(screen, RED, (375, 175), (410, 150), 1)#bras droit
        pygame.draw.line(screen, RED, (375, 250), (340, 275), 1)#jambe gauche
        pygame.draw.line(screen, RED, (375, 250), (410, 275), 1)#jambe droite
        #Partie poto
        pygame.draw.rect(screen, BLACK, (175, 50, 200, 2))#horizontale
        pygame.draw.rect(screen, BLACK, (175, 50, 2, 300))#verticale
        pygame.draw.rect(screen, BLACK, (100, 350, 300, 2))#sol
        pygame.draw.line(screen, BLACK, (175, 100), (200, 50), 2) #diagonale
        pygame.display.update()     
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
