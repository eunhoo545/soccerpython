import pygame
import math
import sys
import random
import numpy as np


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 짝대기 설정
stick_length = 150
stick_width = 10
stick_x = width // 2
stick_y = height - 50  # 바닥에서 조금 위에 위치

# 중력 및 학습 설정
gravity = 0.02
learning_rate = 0.05
discount_factor = 0.95
epsilon = 0.9  # 점점 감소시킬 예정
# Q-table 초기화
num_states = 20  # 예를 들어, 각도를 20개 상태로 나눔
num_actions = 2  # 오른쪽(0) 또는 왼쪽(1)으로 힘을 가함
Q = np.zeros((num_states, num_actions))

def get_state(angle):
    # 각도를 상태로 변환 
    state = int((angle + math.pi/2) / (math.pi / num_states))
    return min(max(state, 0), num_states - 1)

def choose_action(state):
    # greedy한 방법으로 행동 선택
    if random.random() < epsilon:
        return random.randint(0, num_actions - 1)
    else:
        return np.argmax(Q[state])

def update(angle, action):
    # 각도 업데이트 로직
    force = 0.05 if action == 0 else -0.05
    new_angle = angle + force
    new_angle = max(min(new_angle, math.pi/2), -math.pi/2)
    return new_angle

def compute_reward(angle):
    # 보상 계산
    if abs(angle) > math.pi / 2 - 0.1:  # 거의 90도에 도달한 경우
        return -100  # 큰 음의 보상
    return -abs(math.degrees(angle))  # 각도를 도단위로 변환 후 절대값 취함

def draw_stick(angle):
    end_x = stick_x + stick_length * math.sin(angle)
    end_y = stick_y - stick_length * math.cos(angle)
    pygame.draw.line(screen, (255, 0, 0), (stick_x, stick_y), (end_x, end_y), stick_width)

# 게임 루프 및 학습
running = True
angle = math.radians(random.uniform(-45, 45))  # 초기 각도 는 -45에서 45
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((57,129,69))
    state = get_state(angle)
    action = choose_action(state)
    angle = update(angle, action)
    reward = compute_reward(angle)
    next_state = get_state(angle)

    # Q-value 업데이트
    best_future_q = np.max(Q[next_state])
    Q[state, action] += learning_rate * (reward + discount_factor * best_future_q - Q[state, action])

    if abs(angle) > math.pi / 2 - 0.1:  # 막대기가 넘어진 경우
        print('넘어짐')
        angle = math.radians(random.uniform(-45, 45))  # 각도 재설정

    draw_stick(angle)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
