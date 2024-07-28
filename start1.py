import pygame
import sys
import random
import soccer1
# 초기화
pygame.init()

# 화면 크기 및 색상 설정
width, height = 1800, 1000
white = (255, 255, 255)
black = (0, 0, 0)
button_color = (57,129,69)
button_hover_color = (57,150,69)
button_width, button_height = 150, 50

# 화면 설정
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move Window Example")

# 버튼 설정
button_x, button_y = 1500,200
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# 이동할 위치 (상대적)
move_x, move_y = 100, 100

def draw_button():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)
    

def main():
    global button_x, button_y, screen, button_rect
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # 버튼 클릭 시 창 이동
                    button_x += random.randint(-100,100)
                    button_y += random.randint(-100,100)
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    pygame.display.set_mode((width, height))  # 화면 크기 리셋
                    button_rect.topleft = (button_x, button_y)
                    soccer1.main()
        screen.fill((57,129,69))
        draw_button()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
