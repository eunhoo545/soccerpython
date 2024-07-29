import pygame
import sys
import random
import soccer1
# 초기화
pygame.init()
font = pygame.font.SysFont('msgothic',20,False,False)
# 화면 크기 및 색상 설정
width, height = 1800, 1000
white = (255, 255, 255)
black = (0, 0, 0)
button_color = (0,0,0)
button_hover_color = (0,20,0)
button_width, button_height = 150, 50

# 화면 설정
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move Window Example")

# 버튼 설정
button_x, button_y = 900,500
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button2_x, button2_y = 900,650
button2_rect = pygame.Rect(button2_x, button2_y, button_width, button_height)

# 이동할 위치 (상대적)
move_x, move_y = 100, 100

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

def main():
    global button_x, button_y, screen, button_rect, button2_x, button2_y, button2_rect
    clock = pygame.time.Clock()
    running = True

    while running:
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
                    soccer1.main()
                if button2_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        screen.fill((57,129,69))
        text = font.render('Play',0,(255,255,255))
        text2 = font.render('Quit',0,(255,255,255))
        #text3 = font.render('Settings',0,(255,255,255))
        draw_button()
        screen.blit(text,[930,515])
        screen.blit(text2,[900,650])
        pygame.display.flip()
        clock.tick(30)
        

if __name__ == "__main__":
    main()
