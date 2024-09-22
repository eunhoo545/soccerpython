import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Multiple Dropdown Example")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.Font(None, 32)

# 드롭다운 설정
options = ["High", "Mid", "Low"]
dropdown_settings = [
    ("선수1", pygame.Rect(150, 50, 140, 32)),
    ("선수2", pygame.Rect(150, 100, 140, 32)),
    ("선수3", pygame.Rect(150, 150, 140, 32)),
    ("선수4", pygame.Rect(150, 200, 140, 32)),
    ("선수5", pygame.Rect(150, 250, 140, 32)),
    ("선수6", pygame.Rect(150, 300, 140, 32)),
    ("선수7", pygame.Rect(150, 350, 140, 32)),
    ("선수8", pygame.Rect(150, 400, 140, 32)),
    ("선수9", pygame.Rect(150, 450, 140, 32)),
    ("선수10", pygame.Rect(150, 500, 140, 32)),
    ("선수11", pygame.Rect(150, 550, 140, 32)),
]

#Rectangle 객체 선언 11개

color_inactive = GRAY
color_active = BLACK

dropdown_active = [False] * len(dropdown_settings)
#[False, False, False, False, ... False] 
selected_options = [options[0]] * len(dropdown_settings)
#초기값 셋팅

# 드롭다운 항목 설정
option_rects = []
for i in range(len(dropdown_settings)):
    rects = []
    for j, option in enumerate(options):
        rects.append(pygame.Rect(150, 82 + i*50 + j*32, 140, 32))
    option_rects.append(rects)

# 메인 루프

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (label, rect) in enumerate(dropdown_settings):
                if rect.collidepoint(event.pos):
                    dropdown_active[i] = not dropdown_active[i]
                else:
                    dropdown_active[i] = False
                for j, option_rect in enumerate(option_rects[i]):
                    if option_rect.collidepoint(event.pos) and dropdown_active[i]:
                        selected_options[i] = options[j]
                        dropdown_active[i] = False
            if rects[i].collidepoint(event.pos):
                dropdown_active[i]= not dropdown_active[i]
                print(dropdown_active[i])
            else:
                dropdown_active[i] = False
                print(dropdown_active[i])
    screen.fill(WHITE)
    # 드롭다운 메뉴 렌더링
    for i, (label, rect) in enumerate(dropdown_settings):
        pygame.draw.rect(screen, color_active if dropdown_active[i] else color_inactive, rect, 2)
        txt_surface = font.render(selected_options[i], True, BLACK)
        screen.blit(txt_surface, (rect.x + 5, rect.y + 5))
        label_surface = font.render(label, True, BLACK)
        screen.blit(label_surface, (rect.x - 140, rect.y + 5))
        
        if dropdown_active[i]:
            for j, option_rect in enumerate(option_rects[i]):
                pygame.draw.rect(screen, GRAY, option_rect)
                txt_surface = font.render(options[j], True, BLACK)
                screen.blit(txt_surface, (option_rect.x + 5, option_rect.y + 5))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
