import pygame
import sys
import math

# 초기 설정
pygame.init()
clock = pygame.time.Clock()

# 화면 설정
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 플레이어 셋업
player_radius = 25
player_x = screen_width / 2
player_y = screen_height / 2
player_speed = 5
player_color = RED

# 공 셋업
ball_radius = 15
ball_x = screen_width / 2
ball_y = screen_height / 2 - 100
ball_speed = 0  #초기 속도는 0으로 시작
ball_color = GREEN
ball_moving = False
ball_following = False #처음에는 안따라다님

#슈팅, 패스 변수들
power = 0
max_power = 20
power_growing = False

# 각도계산
def calculate_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

# 거리계산
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ball_following:
                power_growing = True
                ball_following = False  # 스페이스를 누르면 공이 따라다니지 않음
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and ball_following:
                power_growing = False
                ball_speed = power
                power = 0
                ball_moving = True
                ball_angle = calculate_angle(player_x, player_y, ball_x, ball_y)
                ball_following = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed

    # 플레이어가 공 가까이 갔을 때 
    if calculate_distance(player_x, player_y, ball_x, ball_y) < player_radius + ball_radius + 10:
        ball_following = True

    # 공이 플레이어를 따라가는 로직
    if ball_following and not ball_moving:
        ball_angle = calculate_angle(player_x, player_y, ball_x, ball_y)
        ball_x += math.cos(ball_angle) * 2
        ball_y += math.sin(ball_angle) * 2

    # 공 이동 로직
    if ball_moving:
        ball_x += math.cos(ball_angle) * ball_speed
        ball_y += math.sin(ball_angle) * ball_speed
        ball_speed *= 0.98  # 공의 속도를 점점 감소시킴
        if ball_speed < 0.5:
            ball_moving = False
            ball_following = False

    # 파워 게이지 증가
    if power_growing and power < max_power:
        power += 0.5

    # 화면 업데이트
    screen.fill(BLACK)
    pygame.draw.circle(screen, player_color, (int(player_x), int(player_y)), player_radius)
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    #PowerBar
    pygame.draw.rect(screen, RED, (20, 20, 20, 200))
    pygame.draw.rect(screen, GREEN, (20, 220 - (power / max_power) * 200, 20, (power / max_power) * 200))

    pygame.display.flip()

    clock.tick(60)  #60프레임