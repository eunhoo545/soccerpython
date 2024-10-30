import pygame
import sys
import time
import math

import menu
from map import lines
from game import throwin,goalkick,kickoff,calculate_angle
import numpy as np
import random
import pickle  # Q-테이블을 파일로 저장하고 불러오기 위한 모듈
import settings

FPS = 1200
MAX_WIDTH = 1800
MAX_HEIGHT = 1000

PASS_FORWARD_REWARD = 6000
PASS_REWARD = 1000
SHOOT_REWARD = 2000

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

GOAL_Y_MIN = 355
GOAL_Y_MAX = 655

F_HOME_FW_START_X = 1000
F_HOME_FW_END_X = 1700

D_HOME_FW_START_X = 600
D_HOME_FW_END_X = 900

F_HOME_MF_START_X = 800
F_HOME_MF_END_X = 1500

D_HOME_MF_START_X = 300
D_HOME_MF_END_X = 700

F_HOME_DF_START_X = 300
F_HOME_DF_END_X = 900

D_HOME_DF_START_X = 50
D_HOME_DF_END_X = 600

F_AWAY_FW_START_X = 100
F_AWAY_FW_END_X = 800

D_AWAY_FW_START_X = 900
D_AWAY_FW_END_X = 1200

F_AWAY_MF_START_X = 300
F_AWAY_MF_END_X = 1000

D_AWAY_MF_START_X = 300
D_AWAY_MF_END_X = 700

F_AWAY_DF_START_X = 900
F_AWAY_DF_END_X = 1500

D_AWAY_DF_START_X = 1200
D_AWAY_DF_END_X = 1850


pi = 180

ball_moving = False
ball_angle = 0
current_holder = None

pass_player = None
pass_in_progress = False
pass_target_player = None
pass_state = None

shoot_in_progress = False
shoot_player = None
last_action = None

homescore = 0
awayscore = 0

screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
myFont = pygame.font.SysFont( "centurygothic", 15, False, False)
startf = pygame.font.SysFont( "centurygothic", 50, True, False)
goalpost1 = pygame.image.load('goalpost1.png')
goalpost2 = pygame.image.load('goalpost1.png')
class Setpiece:
    def throwin(playingteam, givingplayer, startballx, startbally):
        playingteam = playingteam
        givingplayer = givingplayer
        startballx = startballx
        startbally = startbally
    def goalkick(playingteam, givingplayer, startballx, startbally):
        playingteam = playingteam
        givingplayer = givingplayer
        startballx = startballx
        startbally = startbally
    def kickoff(playingteam, givingplayer):
        playingteam = playingteam
        givingplayer = givingplayer
class Agent:
    def __init__(self, actions, learning_rate=0.01, discount_factor=0.9, epsilon=0.1):
        self.q_table = {}
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def get_state(self, environment, player):
        # 상태를 더 큰 그리드로 양자화
        ball_position = (environment.ball.x // 100, environment.ball.y // 100)

        # 현재 플레이어의 위치
        player_position = (player.x // 100, player.y // 100)

        # 공과의 거리
        distance_to_ball = int(distance(player.x, player.y, environment.ball.x, environment.ball.y) // 100)

        # 공을 소유하고 있는지 여부
        has_ball = player.ball_following

        if player.team == 'home':
            opponents = environment.awayteam
        else:
            opponents = environment.hometeam
        closest_opponent = min(opponents, key=lambda p: distance(p.x, p.y, player.x, player.y))
        distance_to_opponent = int(distance(player.x, player.y, closest_opponent.x, closest_opponent.y) // 100)

        return (player_position, ball_position, distance_to_ball, has_ball, distance_to_opponent)

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        else:
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default=np.random.choice(self.actions))

    def learn(self, state, action, reward, next_state):
        prev_value = self.q_table.get(state, {}).get(action, 0)
        future_value = max(self.q_table.get(next_state, {}).values(), default=0)
        self.q_table.setdefault(state, {})[action] = prev_value + self.lr * (reward + self.gamma * future_value - prev_value)

    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty Q-table.")



class Environment:      #환경
    def __init__(self, hometeam, awayteam, ball):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.ball = ball

    def get_positions(self):
        players = self.hometeam + self.awayteam
        distances = [(distance(player.x, player.y, self.ball.x, self.ball.y), player) for player in players]
        distances.sort(key=lambda x: x[0])
        closest_players = distances[:3]
        positions = [(player.x // 100 * 100, player.y // 100 * 100) for _, player in closest_players]
        positions.append((self.ball.x // 100 * 100, self.ball.y // 100 * 100))
        return positions


def pass_completed():
    global current_holder, pass_target_player, pass_in_progress, pass_player
    if pass_in_progress and current_holder == pass_target_player:
        pass_in_progress = False
        print("pass완료!!")
        if current_holder.team == 'home':
            if pass_target_player.x > pass_player.x:  # 홈팀의 패스가 앞쪽(오른쪽)으로 이루어진 경우
                return 'forward'
            return 'normal'
        elif current_holder.team == 'away':
            if pass_target_player.x < pass_player.x:  # 어웨이팀의 패스가 앞쪽(왼쪽)으로 이루어진 경우
                return 'forward'
            return 'normal'
    return False

def render_goal_message(team):
    font = pygame.font.Font(None, 74)
    text = font.render(team+"GOAL !!", True, (0,0,0))
    text_rect = text.get_rect()
    text_rect.center = (900,500)
    screen.blit(text, text_rect)
    pygame.display.update()
    print("Rendered GOAL MESSAGE")
    clock.tick(0.5)

def shoot_completed(ball):
    global homescore
    global awayscore

    home_goal_x = 111
    away_goal_x = 1687

    if GOAL_Y_MIN <= ball.y <= GOAL_Y_MAX:
        if ball.x <= ball.radius + home_goal_x:
            print("슛 성공: 어웨이팀 골!")
            homescore += 1
            return True
        elif ball.x >= away_goal_x - ball.radius:
            print("슛 성공: 홈팀 골!")
            awayscore += 1
            return True
    return False

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def calculate_angle(x1, y1, x2, y2):        #각도계산
    return math.atan2(y2 - y1, x2 - x1)


def calculate_reward(action, environment, player):
    global current_holder, last_action, pass_in_progress, pass_target_player, ball_angle, pass_player
    reward = -1

    if action == 'intercept' and current_holder != player and current_holder is not None:
        if player.team != current_holder.team and distance(player.x, player.y, environment.ball.x, environment.ball.y) < player.radius + environment.ball.radius:
            reward = 50
    
    # if action in ['move_left', 'move_right']:
    #     if current_holder == player:
    #         if player.team == 'home' and action == 'move_right':
    #             reward = 10
    #         elif player.team == 'away' and action == 'move_left':
    #             reward = 10
    #         else:
    #             reward = -10

    if action in ['move_left', 'move_right']:
        if current_holder is not None:
            if current_holder.team == 'home' and player.team == 'home':
                if player.role == 'FW':
                    if F_HOME_FW_START_X < player.x and player.x < F_HOME_FW_END_X:
                        print("FW REWARD")
                        reward = 20
                    else: 
                        if action == 'move_right':
                            if player.x < F_HOME_FW_END_X:
                                reward = player.x/100
                        else:   
                            reward = (player.x/100)*(-1)
                elif player.role == 'MF':
                    if F_HOME_MF_START_X < player.x and player.x < F_HOME_MF_END_X:
                        print("MF REWARD")
                        reward = 20
                    else: 
                        if action == 'move_right':
                            if player.x < F_HOME_MF_END_X:
                                reward = player.x/100
                        else:   
                            reward = (player.x/100)*(-1)
                elif player.role == 'DF':
                    if F_HOME_DF_START_X < player.x and player.x < F_HOME_DF_END_X:
                        print("DF REWARD")
                        reward = 20
                    else: 
                        if action == 'move_right':
                            if player.x < F_HOME_DF_END_X:
                                reward = player.x/100
                        else:
                            reward = (player.x/100)*(-1)
            elif current_holder.team == 'away' and player.team == 'home':
                if player.role == 'FW':
                    if D_HOME_FW_START_X < player.x and player.x < D_HOME_FW_END_X:
                        reward = 20
                    else: 
                        if action == 'move_left':
                            reward = 18 - (player.x/100)
                        else:
                            reward = (player.x/100)*(-1) - 18
                elif player.role == 'MF':
                    if D_HOME_MF_START_X < player.x and player.x < D_HOME_MF_END_X:
                        reward = 20
                    else:
                        if action == 'move_left':
                            reward = 18 - (player.x/100)
                        else:
                            reward = (player.x/100)*(-1) - 18
                elif player.role == 'DF':
                    if D_HOME_DF_START_X < player.x and player.x < D_HOME_DF_END_X:
                        reward = 20
                    else:
                        if action == 'move_left':
                            reward = 18 - (player.x/100)
                        else:
                            reward = (player.x/100)*(-1) - 18


                            
            elif current_holder.team == 'away' and player.team == 'away': #away공격
                if player.role == 'FW':
                    if F_AWAY_FW_START_X < player.x and player.x < F_AWAY_FW_END_X:
                        print("FW REWARD")
                        reward = 20
                    else: 
                        if action == 'move_left':
                            if player.x > F_AWAY_FW_START_X:
                                reward = (18 - player.x/100)
                        else:   
                            reward = (18 - player.x/100)*(-1)
                elif player.role == 'MF':
                    if F_AWAY_MF_START_X < player.x and player.x < F_AWAY_MF_END_X:
                        print("MF REWARD")
                        reward = 20
                    else: 
                        if action == 'move_left':
                            if player.x > F_AWAY_MF_START_X:
                                reward = (18 - player.x/100)
                        else:   
                            reward = (18 - player.x/100)*(-1)
                elif player.role == 'DF':
                    if F_AWAY_DF_START_X < player.x and player.x < F_AWAY_DF_END_X:
                        print("DF REWARD")
                        reward = 20
                    else: 
                        if action == 'move_left':
                            if player.x > F_AWAY_DF_START_X:
                                reward = (18 - player.x/100)
                        else:   
                            reward = (18 - player.x/100)*(-1)
            elif current_holder.team == 'home' and player.team == 'away': #away수비
                if player.role == 'FW':
                    if D_AWAY_FW_START_X < player.x and player.x < D_AWAY_FW_END_X:
                        reward = 20
                    else: 
                        if action == 'move_right':
                            reward = player.x/100
                        else:
                            reward = (player.x/100)*-1
                elif player.role == 'MF':
                    if D_AWAY_MF_START_X < player.x and player.x < D_AWAY_MF_END_X:
                        reward = 20
                    else: 
                        if action == 'move_right':
                            reward = player.x/100
                        else:
                            reward = (player.x/100)*-1
                elif player.role == 'DF':
                    if D_AWAY_DF_START_X < player.x < D_AWAY_DF_END_X:
                        reward = 20
                    else:
                        if action == 'move_left':
                            reward = player.x/100
                        else:
                            reward = (player.x/100)*(-1)  
                                         
    print(reward)
    return reward



def setup_teams_and_ball():
    global hometeam
    global awayteam
    # 플레이어 생성
    hometeam = [
        Person(1,15, 738, 502, 'home', RED, role='FW'),
        Person(2,15, 690, 684, 'home', RED, role='MF'),
        Person(3,15, 758, 808, 'home', RED, role='FW'),
        Person(4,15, 724, 158, 'home', RED, role='FW'),
        Person(5,15, 600, 310, 'home', RED, role='MF'),
        Person(6,15, 402, 108, 'home', RED, role='DF'),
        Person(7,15, 358, 632, 'home', RED, role='DF'),
        Person(8,15, 318, 388, 'home', RED, role='DF'),
        Person(9,15, 458, 860, 'home', RED, role='DF'),
        Person(10,15, 166, 506, 'home', RED, role='GK')
    ]
    awayteam = [
        Person(1,15, 1030, 396, 'away', BLUE,role='FW'),
        Person(2,15, 1050, 612, 'away', BLUE,role='FW'),
        Person(3,15, 1042, 828, 'away', BLUE,role='FW'),
        Person(4,15, 1082, 204, 'away', BLUE, role='FW'),
        Person(5,15, 1240, 458, 'away', BLUE, role='MF'),
        Person(6,15, 1220, 650, 'away', BLUE, role='MF'),
        Person(7,15, 1362, 864, 'away', BLUE, role='DF'),
        Person(8,15, 1300, 134, 'away', BLUE, role='DF'),
        Person(9,15, 1406, 368, 'away', BLUE, role='DF'),
        Person(10,15, 1446, 670, 'away', BLUE, role='DF'),
        Person(11,15, 1624, 498, 'away', BLUE, role='GK')
    ]
    # 공 생성
    global ball
    ball = Ball(12)
    return hometeam, awayteam, ball


def moveplayer(cplayer,keys,setting,ball):
    #print(cplayer.x,cplayer.y)
    if keys[pygame.K_a]:
        cplayer.x -= int(setting['redrunspeed']) * 0.8
    if keys[pygame.K_d]:
        cplayer.x += int(setting['redrunspeed']) * 0.8
    if keys[pygame.K_w]:
        cplayer.y -= int(setting['redrunspeed']) * 0.8
    if keys[pygame.K_s]:
        cplayer.y += int(setting['redrunspeed']) * 0.8      #플레이어 움직이기
    if keys[pygame.K_SPACE]:
        cplayer.pass2(ball)
    if keys[pygame.K_f]:
        cplayer.search()
    if keys[pygame.K_r]:
        cplayer.intercept(ball)
 
def move_towards_ball(player, ball, speed):
    angle = calculate_angle(player.x, player.y, ball.x, ball.y)
    player.x += math.cos(angle) * speed
    player.y += math.sin(angle) * speed

def main(width,height):
    global homescore, awayscore
    global ball_moving
    global ball_angle
    global pass_in_progress, shoot_in_progress
    global pass_target_player

    screen = pygame.display.set_mode((width, height))
    me = Person(11,15, 930, 502, 'home', GREEN, role='FW')
    setpiece = Setpiece()
    screen.fill((48, 131, 43))

    hometeam = []
    awayteam = []

    hometeam, awayteam, ball = setup_teams_and_ball()
    environment = Environment(hometeam, awayteam, ball)

    agents = {}
    for player in hometeam + awayteam:
        agents[player] = Agent(actions=['move_left', 'move_right', 'move_up', 'move_down', 'pass', 'search', 'intercept', 'shoot'])
        agents[player].load_q_table(f'./qtable/q_table_{player.team}_{player.number}.pkl')
    
    startt = startf.render('test',True,(255,255,255))
    ball = Ball(12)
    start_time = time.time()

    while True:
        global setting
        setting = settings.load_setting()
        keys = pygame.key.get_pressed()
        moveplayer(me,keys,setting,ball)
        global homescore
        global awayscore
        goal_y_min = 355
        goal_y_max = 655
        home_goal_x = 111
        away_goal_x = 1687
                
        if time.time() - start_time > 120:  # 120초가 지나면 Q-테이블 저장 및 게임 재시작
            agent.save_q_table('q_table.pkl')
            main(1800,1000)
            return
        def game_start():
            if time.time() - start_time > 0:
                return True
            return False

        if game_start():
            global current_holder
            for person in hometeam + awayteam:  # 모든 플레이어 조회
                agent = agents[person]
                state = agent.get_state(environment, person)  # 위치를 불러온다 (state 획득)
                action = agent.choose_action(state)  # 할 행동을 고른다
                # 행동 실행
                if action == 'move_up':
                    person.moveup()
                elif action == 'move_down':
                    person.movedown()
                elif action == 'move_left':
                    person.moveleft()
                elif action == 'move_right':
                    person.moveright()  # 플레이어가 움직이는 액션일 경우의 처리
                if person.ball_following:  # 플레이어가 공을 잡고있을때
                    if action == 'pass':
                        teammates = []
                        if person in hometeam:
                            teammates = [p for p in hometeam if p != person] + [me]
                        else:
                            teammates = [p for p in awayteam if p != person]  # 플레이어가 패스
                        if teammates:
                            target_player = random.choice(teammates)  # 랜덤으로 패스받을 선수 선택
                            person.pass1(ball, target_player, state)  # 패스
                            pass_target_player = target_player
                    elif action == 'search':  # 액션이 search 일때 처리
                        person.search()  # search 함수
                    elif action == 'shoot':  # 액션이 shoot일때
                        x1 = 0
                        x2 = 0
                        y1 = 0
                        y2 = 0

                        if current_holder is not None:
                            if current_holder.team == 'away':  # 공을 잡고있는 선수가 away 팀일때 골대의 위치
                                x1 = 18
                                x2 = 111
                                y1 = 354
                                y2 = 657
                            if current_holder.team == 'home':  # 공을 잡고있는 선수가 home 팀일때 골대의 위치
                                x1 = 1691
                                x2 = 1786
                                y1 = 354
                                y2 = 657

                            if abs(distance(current_holder.x, current_holder.y, (x1 + x2) / 2, (y1 + y2) / 2)) < 800:  # 공을 잡은 플레이어와 목표 골대사이의 거리가 800보다 작을때
                                current_holder.shoot1(ball, x1, x2, y1, y2,state)  # 목표 골대로 슛
                else:
                    if action == 'intercept':  
                        person.intercept(ball)

                # 보상 계산 및 학습
                reward = calculate_reward(action, environment, person)  # 어떤 액션에 대한 보상
                next_state = agent.get_state(environment, person)  # 액션 이후의 state 가져오기
                agent.learn(state, action, reward, next_state)  # 학습
            
            if pass_in_progress:
                global pass_state
                pass_result = pass_completed()
                if pass_result == 'forward':
                    next_state = agent.get_state(environment, person)
                    agent.learn(pass_state, action, PASS_FORWARD_REWARD, next_state)
                    print("forward 보상 지급 완료")
                elif pass_result == 'normal':
                    next_state = agent.get_state(environment, person)
                    agent.learn(pass_state, action, PASS_REWARD, next_state)
                    print("일반 보상 지급 완료")

            if shoot_in_progress:
                global shoot_state
                shoot_result = shoot_completed(ball)
                if shoot_result and shoot_player is not None:
                    next_state = agent.get_state(environment, shoot_player)
                    agent.learn(shoot_state, 'shoot', SHOOT_REWARD, state)
                    shoot_in_progress = False

            if not any(player.ball_following for player in hometeam + awayteam + [me]):  # 공을 따라가고 있는 플레이어가 없음
                    filtered_home_team = [player for player in hometeam if player != pass_player]+[me]
                    filtered_away_team = [player for player in awayteam if player != pass_player]
                    if filtered_home_team:
                        closest_home_player = min(filtered_home_team, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
                        move_towards_ball(closest_home_player, ball, closest_home_player.speed)

                    if filtered_away_team:
                        closest_away_player = min(filtered_away_team, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
                        move_towards_ball(closest_away_player, ball, closest_away_player.speed)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for player in hometeam + awayteam:
                        agent = agents[player]
                        agent.save_q_table(f'./qtable/q_table_{player.team}_{player.number}.pkl')
                    pygame.quit()
                    sys.exit()

            if ball_moving:
                ball.rotate(3)
                ball.x += math.cos(ball_angle) * ball.speed
                ball.y += math.sin(ball_angle) * ball.speed
                ball.speed *= 0.99
                if ball.speed < 0.2:
                    ball_moving = False

            
                
            for i in hometeam + [me] + awayteam:
                if i.ball_following:
                    ball.x = i.x + math.cos(ball_angle) * 12
                    ball.y = i.y + math.sin(ball_angle) * 12

            for i in hometeam + [me] + awayteam:
                d = distance(i.x, i.y, ball.x, ball.y)
                if 0 <= d and d < ball.radius + i.radius and ball.speed < 3:
                    i.ball_following = True
                    current_holder = i
                else:
                    i.ball_following = False
                    
            
            
            if ball.x < 50:
                ball.x = 50
            if ball.x > 1750:
                ball.x = 1750
            if ball.y < 20:
                ball.y = 20
            if ball.y > 980:
                ball.y = 980

            clock.tick(FPS)
            screen.fill((48, 131, 43))

            lines()
            me.draw()
            for i in range(len(hometeam)):
                hometeam[i].draw()
            for j in range(len(awayteam)):
                awayteam[j].draw()
            ball.draw(current_holder,screen)
            scoretext = myFont.render((str(homescore) + str(' - ') + str(awayscore)), True, (0, 0, 0))
            pygame.draw.line(screen, (255, 255, 255), (0, 5), (30, 5), 10)
            pygame.transform.flip(goalpost2, True, False)
            screen.blit(scoretext, [173, 56])
            if GOAL_Y_MIN <= ball.y <= GOAL_Y_MAX:
                if ball.x <= ball.radius + home_goal_x:
                    print("슛 성공: 어웨이팀 골!")
                    awayscore += 1
                    render_goal_message('away')
                    main(1800,1000)
                elif ball.x >= away_goal_x - ball.radius:
                    print("슛 성공: 홈팀 골!")
                    homescore += 1
                    render_goal_message('home')
                    main(1800,1000)
            screen.blit(goalpost1, [1300, 285])
            screen.blit(goalpost2, [-373, 285])
            pygame.display.update()
        else:
            screen.fill((255,255,255))
            screen.blit(startt, [900,500])

class Ball(): #공
    def __init__(self,radius):
        self.x = 1100
        self.y = 505
        self.radius = radius
        self.speed = 0
        self.angle = 0
        self.image = pygame.image.load("ball.png")  # 이미지 불러오기
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))  # 원 크기에 맞게 이미지 크기 조정

    def draw(self,person, screen):
        image_rect =self.image.get_rect()
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))  # 중심을 유지하면서 회전
        if person is not None and person.ball_following == True:
            dx = person.x - self.x
            dy = person.y - self.y
            #pygame.draw.circle(screen,(0,0,0),(self.x-(dx),self.y-(dy)),self.radius)
            rotated_rect.center = (self.x - dx, self.y - dy)
            screen.blit(rotated_image, rotated_rect)
        else:
            #pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius)
            screen.blit(rotated_image, rotated_rect) #이미지 그리기
    def rotate(self, angle_speed):
        self.angle += angle_speed




class Person():
    def __init__(self,number,radius,x,y,team,color=GREEN,role='def'):
        self.number = number
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 2
        self.team = team
        self.color = color
        self.ball_following = False
        self.role = role

    def distance(x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def get_closest_player(self,environment):
        if self.team == 'home':
            teammates = environment.hometeam
        else:
            teammates = environment.awayteam
        closest_player = min(
            (p for p in environment.hometeam if p != self),
            key=lambda p: distance(self.x, self.y, p.x, p.y),
            default=None
        )
        dist = distance(self.x, self.y, closest_player.x, closest_player.y)

        return dist
    def moveup(self):
        self.y -= self.speed
    def movedown(self):
        self.y += self.speed
    def moveright(self):
        self.x += self.speed
    def moveleft(self):
        self.x -= self.speed

    def search(self):
        global ball_angle
        if self.ball_following:
            ball_angle += pi/1800
            if ball_angle >= 6.28:
                ball_angle = 0

    def pass2(self,ball):
        if self.ball_following:
            global ball_moving
            self.ball_following = False
            ball_moving = True
            ball.speed = int(setting['bluepasspower']) * 0.7

    def pass1(self, ball, target_player, state):
        if self.ball_following:
            global ball_moving, pass_player, pass_in_progress, pass_state
            self.search()
            angle = calculate_angle(self.x, self.y, target_player.x, target_player.y)
            angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
            angle_difference = abs(angle - angle_ball)
            if angle_difference < 0.1:  # 0.1 라디안 이내의 차이를 허용
                print(f"패스 시도: {self.team}팀 의 {self.number}선수가 {target_player.team}팀의 {target_player.number} 의 선수에게 패스")
                self.ball_following = False
                ball_moving = True
                pass_in_progress = True
                pass_player = self
                print("패스 시도한 player: ",pass_player.number)
                pass_state = state
                if current_holder in hometeam:
                    ball.speed = int(setting['redpasspower']) * 0.8
                elif current_holder in awayteam:
                    ball.speed = int(setting['bluepasspower']) * 0.8


    def shoot1(self, ball, x1, x2, y1, y2,state):
        global shoot_player, shoot_in_progress, shoot_state
        if self.ball_following:
            global ball_moving
            angle = calculate_angle(self.x, self.y, (x1 + x2) / 2, (y1 + y2) / 2)
            angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
            angle_difference = abs(angle - angle_ball)
            if angle_difference < 0.2:  # 0.2 라디안 이내의 차이를 허용
                ball_moving = True
                shoot_in_progress = True
                shoot_player = self
                shoot_state = state
                print(f"슛 시도: {self.team}팀 의 {self.number}선수가 슛")
                self.ball_following = False
                if current_holder in hometeam:
                    ball.speed = int(setting['redshootpower']) * 2
                elif current_holder in awayteam:
                    ball.speed = int(setting['bluepasspower']) * 2


    def calculate_angle(x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)

    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

    def intercept(self, ball):
        global current_holder
        if current_holder is not None:
            if (not self.ball_following) and (self.team != current_holder.team):
                if distance(ball.x,ball.y,self.x,self.y)<=50 and random.randint(0,2)<1:
                    self.ball_following = True
                    return

        if current_holder is not None:
            if (not self.ball_following) and (self.team != current_holder.team):
                move_towards_ball(self, ball, self.speed)

        
if __name__ == '__main__':
    main(1800,1000)