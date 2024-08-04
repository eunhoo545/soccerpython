import pygame
import sys
import random
import soccer1
import start1
pygame.init()
width, height = 1800, 1000

screen = pygame.display.set_mode((width, height))
white = (255, 255, 255)
black = (0, 0, 0)
button_color = (0,0,0)
button_hover_color = (0,20,0)
button_width, button_height = 150, 50
button_x, button_y = 900,500
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
button2_x, button2_y = 900,575
button2_rect = pygame.Rect(button2_x, button2_y, button_width, button_height)

def draw_button():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if button2_rect.collidepoint((mouse_x, mouse_y)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(screen, button_hover_color, button2_rect)
    else:
        pygame.draw.rect(screen, button_color, button2_rect)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    #if button2_rect.collidepoint((mouse_x, mouse_y)):
    #    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    #    pygame.draw.rect(screen, button_hover_color, button3_rect)
    #else:
    #    pygame.draw.rect(screen, button_color, button3_rect)
    #    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)   
font = pygame.font.SysFont('msgothic',20,False,False)


def main():
    global button_x, button_y, screen, button_rect, button2_x, button2_y, button2_rect
    clock = pygame.time.Clock()
    running = True

    while running:
        print(soccer1.X)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # 버튼 클릭 시 창 이
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    pygame.display.set_mode((width, height))  # 화면 크기 리셋
                    button_rect.topleft = (button_x, button_y)
                    start1.main()
                if button2_rect.collidepoint(event.pos):
                    if soccer1.X == True:
                        soccer1.X = False
                    else:
                        soccer1.X = True
                #if button3_rect.collidepoint(event.pos):
                   # print('settings')
                    
        screen.fill((57,129,69))
        text = font.render('BACK',0,(255,255,255))
        text2 = font.render(str(soccer1.X),0,(255,255,255))
        #text3 = font.render('Settings',0,(255,255,255))
        #text3 = font.render('Settings',0,(255,255,255))
        draw_button()
        screen.blit(text,[930,515])
        screen.blit(text2,[930,590])
       #screen.blit(text2,[930,665])
        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()
