import pygame
import numpy as np
import random

pygame.init()
size = (400, 400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

grid_size = 40  # 크기 40짜리 타일
grid_width = size[0] // grid_size  # 가로 타일수
grid_height = size[1] // grid_size  # 세로 타일 수

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 에이전트 및 목표 초기 위치 설정
agent_position = [grid_width // 2, grid_height // 2]
goal_position = [grid_width - 1, grid_height - 1]

# Q-테이블 초기화
actions = ['up', 'down', 'left', 'right']
q_table = np.zeros((grid_width, grid_height, len(actions)))
learning_rate = 0.1
discount_factor = 0.99
epsilon = 0.1

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.choice(actions)  # 무작위 행동 선택
    else:
        action_index = np.argmax(q_table[state[0], state[1]])
        return actions[action_index]  # 최적 행동 선택

def update_state(action):
    new_position = agent_position.copy()
    if action == 'up':
        new_position[1] -= 1
    elif action == 'down':
        new_position[1] += 1
    elif action == 'left':
        new_position[0] -= 1
    elif action == 'right':
        new_position[0] += 1

    # 경계 조건 체크
    if new_position[0] < 0 or new_position[0] >= grid_width or new_position[1] < 0 or new_position[1] >= grid_height:
        return None  # 벽에 부딪힘
    return new_position

def get_reward(new_position):
    if new_position is None:
        return -50  # 벽에 부딪혔을 때 큰 페널티
    elif new_position == goal_position:
        print('도달')
        return 100000  # 목표 도달 보상
    else:
        return -1  # 이동 페널티

# 게임 및 학습 루프
running = True
session_count = 0
while running:
    #if session_count >= 10000:  # 일정 세션 수 이후에 프로그램 종료
        #break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    action = choose_action(agent_position)
    new_position = update_state(action)
    reward = get_reward(new_position)
    
    if new_position is None:  # 벽에 부딪힌 경우
        session_count += 1
        agent_position = [grid_width // 2, grid_height // 2]  # 초기 위치 재설정
        print(f"세션 {session_count}: 벽에 부딫혔습니다. 초기위치로...")
        continue
    if new_position == goal_position:
        session_count +=1
        agent_position = [grid_width // 2, grid_height // 2]  # 초기 위치 재설정
    
    # Q-값 업데이트
    old_value = q_table[agent_position[0], agent_position[1], actions.index(action)]
    future_max_value = np.max(q_table[new_position[0], new_position[1]])
    new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * future_max_value)
    q_table[agent_position[0], agent_position[1], actions.index(action)] = new_value
    #print(old_value,new_value)
    # 에이전트 위치 업데이트
    agent_position = new_position
    
    # 화면
    screen.fill(black)
    for x in range(grid_width):
        for y in range(grid_height):
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, white, rect, 1)
    
    agent_rect = pygame.Rect(agent_position[0] * grid_size, agent_position[1] * grid_size, grid_size, grid_size)
    pygame.draw.rect(screen, red, agent_rect)
    goal_rect = pygame.Rect(goal_position[0] * grid_size, goal_position[1] * grid_size, grid_size, grid_size)
    pygame.draw.rect(screen, white, goal_rect)
    
    pygame.display.flip()
    clock.tick(2000)

pygame.quit()
