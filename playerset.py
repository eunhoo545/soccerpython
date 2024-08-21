import pygame
import sys
import settings



button = pygame.Rect(100,100,200,100)


def playerset():
    
    global screen
    # 초기화
    pygame.init()

    # 화면 설정
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Dropdown Menu Example")

    # 색상 정의
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)

    # 폰트 설정
    font = pygame.font.Font(None, 32)

    # 드롭다운 설정
    options = ["High", "Midi", "Low"]
    dropdown_rect = pygame.Rect(200, 100, 140, 32)
    color_inactive = GRAY
    color_active = BLACK
    color = color_inactive
    active = False
    selected_option = options[0]

    # 드롭다운 항목 설정
    option_rects = []
    for i, option in enumerate(options):
        option_rects.append(pygame.Rect(200, 132 + i*32, 140, 32))

    # 메인 루프
    done = False
    while not done:
        
        print(active)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint(event.pos):
                    active = not active
                for i, option_rect in enumerate(option_rects):
                    if option_rect.collidepoint(event.pos):
                        if active:
                            selected_option = options[i]
                            print(selected_option)
                            active = False
                    color = color_active if active else color_inactive

        screen.fill(WHITE)


        draw(screen)
        # 드롭다운 메뉴 렌더링
        pygame.draw.rect(screen, color, dropdown_rect, 2)
        txt_surface = font.render(selected_option, True, color)
        text1 = font.render('Player1', True, (0,0,0))
        screen.blit(txt_surface, (dropdown_rect.x + 5, dropdown_rect.y + 5))
        screen.blit(text1, (100,100))

        if active:
            for i, option_rect in enumerate(option_rects):
                pygame.draw.rect(screen, GRAY, option_rect)
                txt_surface = font.render(options[i], True, BLACK)
                screen.blit(txt_surface, (option_rect.x + 5, option_rect.y + 5))

        pygame.display.flip()
        pygame.time.Clock().tick(30)
    pygame.quit()
    sys.exit()
def draw(screen):

    pygame.draw.rect(screen, (0,0,0), button)
