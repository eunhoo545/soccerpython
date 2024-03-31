import pygame
pygame.init()
screen = pygame.display.set_mode((1800,1000))
def main():

    while True:
        pygame.draw.line(screen,(255,0,0),(0,0),(30,0))
        screen.fill(255,255,255)
        pygame.display.flip()