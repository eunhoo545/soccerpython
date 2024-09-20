import pygame
import sys
import time
import math

import start1
from map import lines
from game import throwin,goalkick,kickoff,calculate_angle
import numpy as np
import random
import pickle  # Q-테이블을 파일로 저장하고 불러오기 위한 모듈
import settings

FPS = 60
MAX_WIDTH = 1800
MAX_HEIGHT = 1000

PASS_FORWARD_REWARD = 1500
PASS_REWARD = 1000
SHOOT_REWARD = 2000

shoot_start_time = None  # 슛이 시작된 시간을 기록
SHOOT_DELAY = 3  # 슛이 성공 여부를 판단할 지연 시간 (2초)


ball_moving = False
ball_angle = 0
current_holder = None
pass_in_progress = False
pass_target_player = None
shoot_in_progress = False  # 슛 진행 상태를 추적
last_action = None


screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
pi = 180
RED = (255, 0, 0)

myFont = pygame.font.SysFont( "centurygothic", 15, False, False)
startf = pygame.font.SysFont( "centurygothic", 50, True, False)
goalpost1 = pygame.image.load('goalpost1.png')
goalpost2 = pygame.image.load('goalpost1.png')

class Agent:
	def __init__(self, actions, learning_rate=0.01, discount_factor=0.9, epsilon=0.6):
		self.q_table = {}
		self.actions = actions
		self.lr = learning_rate
		self.gamma = discount_factor
		self.epsilon = epsilon

	def get_state(self, environment):
		global closest_away_player
		global closest_home_player
		# 상태를 더 큰 그리드로 양자화
		ball_position = (environment.ball.x // 200, environment.ball.y // 200)

		# 가장 가까운 홈팀과 어웨이팀 선수의 위치
		closest_home_player = min(environment.hometeam, key=lambda p: distance(p.x, p.y, environment.ball.x, environment.ball.y))
		closest_away_player = min(environment.awayteam, key=lambda p: distance(p.x, p.y, environment.ball.x, environment.ball.y))

		home_position = (closest_home_player.x // 200, closest_home_player.y // 200)
		away_position = (closest_away_player.x // 200, closest_away_player.y // 200)

		# 상대적 위치와 공의 위치를 상태로 반환
		return (home_position, away_position, ball_position)

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

	def get_positions(self):        #위치 가져오기
		players = self.hometeam + self.awayteam  
		distances = [(distance(player.x, player.y, self.ball.x, self.ball.y), player) for player in players]        #플레이어들과 공 사이의 거리를 조회해서 리스트에 저장
		distances.sort(key=lambda x: x[0])      #가까운 순서대로 정렬
		closest_players = distances[:3]     #가장 가까운 세명
		positions = [(player.x // 100 * 100, player.y // 100 * 100) for _, player in closest_players]       #가까운 세명의 x와 y좌표를 100단위로 저장
		positions.append((self.ball.x // 100 * 100, self.ball.y // 100 * 100))      
		return positions            #반환


def pass_completed(hometeam, awayteam):
	global current_holder, pass_target_player, pass_in_progress
	current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
	if pass_in_progress and current_holder == pass_target_player:
		print("pass 성공")
		pass_in_progress = False
		if (current_holder.team == 'home' and current_holder.y < pass_target_player.y) or \
		   (current_holder.team == 'away' and current_holder.y > pass_target_player.y):
			return 'forward'
		return 'normal'
	return False



def throwin(person,ball,y,map):
	time.sleep(1)
	#print('throwin')
	map.throwin = True
	ball.x = ball.x
	ball.y = y- ball.radius
	ball_moving= False
	person.ball_following = False
	ball.speed = 0
	person.x = ball.x
	person.y = ball.y +20
def kickoff():
	#print('kickoff')
	time.sleep(1)
def cornerkick():
	#print('cornerkick')
	time.sleep(1)



def shoot_completed(ball):
	goal_y_min = 370
	goal_y_max = 630
	home_goal_x = 0
	away_goal_x = 1800

	if goal_y_min <= ball.y <= goal_y_max:
		if ball.x <= ball.radius + home_goal_x:
			print("슛 성공: 홈팀 골!")
			return True
		elif ball.x >= away_goal_x - ball.radius:
			print("슛 성공: 어웨이팀 골!")
			return True
	return False

def calculate_average_distance(players):
	total_distance = 0
	count = 0
	for i, player1 in enumerate(players):
		for j, player2 in enumerate(players):
			if i < j:
				total_distance += distance(player1.x, player1.y, player2.x, player2.y)
				count += 1
	if count > 0:
		return total_distance / count
	else:
		return float('inf')  # 플레이어가 없으면 무한대 반환

def distance(x1, y1, x2, y2):#거리계산
	return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def calculate_angle(x1, y1, x2, y2):        #각도계산
	return math.atan2(y2 - y1, x2 - x1)
def calculate_reward(action, environment):
	global current_holder, last_action, pass_in_progress, pass_target_player
	current_holder = next((player for player in environment.hometeam + environment.awayteam if player.ball_following), None)
	teammates = [player for player in environment.hometeam if current_holder in environment.hometeam] + \
				[player for player in environment.awayteam if current_holder in environment.awayteam]
	if action == 'pass' and pass_in_progress and current_holder:
		if current_holder.team == 'home':
			if pass_target_player.x > current_holder.x:  # 홈팀의 패스가 앞쪽(오른쪽)으로 이루어진 경우
				return PASS_FORWARD_REWARD
		elif current_holder.team == 'away':
			if pass_target_player.x < current_holder.x:  # 어웨이팀의 패스가 앞쪽(왼쪽)으로 이루어진 경우
				return PASS_FORWARD_REWARD
	# 공을 가진 선수가 상대방 진영으로 이동하는 보상
	if action in ['move_left', 'move_right']:
		if current_holder is not None:
			if current_holder.team == 'home' and action == 'move_right':
				return 1000
			elif current_holder.team == 'away' and action == 'move_left':
				return 1000
		return -900

	if action == 'intercept' and current_holder is None:
		for player in environment.hometeam + environment.awayteam:
			if player.ball_following:
				if player.team != current_holder.team and distance(player.x, player.y, environment.ball.x, environment.ball.y) < player.radius + environment.ball.radius:
					return 150
				
	pass_result = pass_completed(environment.hometeam, environment.awayteam)
	if pass_result == 'forward':
		print("앞쪽 선수에게 패스")
		return PASS_FORWARD_REWARD
	elif pass_result == 'normal':
		print("일반 패스")
		return PASS_REWARD

	# if action == 'shoot':
	#     if shoot_completed():
	#         return SHOOT_REWARD  # 슛 성공 보상
	#     else:
	#         return -1000  # 슛 실패 패널티
	else:
		return -10

	
def setup_teams_and_ball():
	global hometeam
	global awayteam
	# 플레이어 생성
	hometeam = [
		#Person(15, 930, 502, 'home', ),
		Person(15, 738, 502, 'home', ),
		Person(15, 690, 684, 'home', ),
		Person(15, 758, 808, 'home', ),
		Person(15, 724, 158, 'home', ),
		Person(15, 600, 310, 'home', ),
		Person(15, 402, 108, 'home', ),
		Person(15, 358, 632, 'home', ),
		Person(15, 318, 388, 'home', ),
		Person(15, 458, 860, 'home', ),
		Person(15, 166, 506, 'home', )
	]
	awayteam = [
		Person(15, 1030, 396, 'away', ),
		Person(15, 1050, 612, 'away', ),
		Person(15, 1042, 828, 'away', ),
		Person(15, 1082, 204, 'away', ),
		Person(15, 1240, 458, 'away', ),
		Person(15, 1220, 650, 'away', ),
		Person(15, 1362, 864, 'away', ),
		Person(15, 1300, 134, 'away', ),
		Person(15, 1406, 368, 'away', ),
		Person(15, 1446, 670, 'away', ),
		Person(15, 1624, 498, 'away', )
	]
	# 공 생성
	global ball
	ball = Ball(12)    
	return hometeam, awayteam, ball


def goal_scored(ball):
	goal_y_min = 370
	goal_y_max = 630
	home_goal_x = 0
	away_goal_x = 1800

	if (ball.y >= goal_y_min and ball.y <= goal_y_max):
		if ball.x <= ball.radius + home_goal_x:
			return 'away'
		elif ball.x >= away_goal_x - ball.radius:
			return 'home'
	return None

def moveplayer(person,keys,setting,ball):
	
	if keys[pygame.K_a]:
		person.x -= int(setting['redrunspeed']) * 0.1  
	if keys[pygame.K_d]:
		person.x += int(setting['redrunspeed']) * 0.1  
	if keys[pygame.K_w]:
		person.y -= int(setting['redrunspeed']) * 0.1  
	if keys[pygame.K_s]:
		person.y += int(setting['redrunspeed']) * 0.1      #플레이어 움직이기
	if keys[pygame.K_SPACE]:
		person.pass2(ball)
	if keys[pygame.K_f]:
		person.search() 
def move_towards_ball(player, ball, speed):
	angle = calculate_angle(player.x, player.y, ball.x, ball.y)
	player.x += math.cos(angle) * speed
	player.y += math.sin(angle) * speed 

def game_start(start_time):
	if time.time() - start_time > 0:
		return True
	return False

def check_wall(ball):
	if ball.x < 50:         
		ball.x = 50
	if ball.x > 1750:
		ball.x = 1750
	if ball.y < 20:
		ball.y = 20
	if ball.y > 980:
		ball.y = 980 

def main():

	global ball_moving
	global ball_angle
	homescore = 0
	awayscore = 0
	hometeam = []
	awayteam = []

	person = Person(15, 930, 502, 'home', )
	agent = Agent(actions=['move_up', 'move_down', 'move_left', 'move_right', 'kick', 'pass', 'search', 'intercept', 'shoot'], learning_rate=0.01, discount_factor=0.9, epsilon=0.9)
	agent.load_q_table('q_table.pkl')
	hometeam, awayteam, ball = setup_teams_and_ball()
	environment = Environment(hometeam, awayteam, ball)
	scoretext = myFont.render((str(homescore) + str(' - ') + str(awayscore)), True, (0, 0, 0))
	stop = startf.render('stop',True,(255,255,255))
	ball = Ball(12)
	start_time = time.time()
	
	while True:
		global setting
		setting = settings.load_setting()
		keys = pygame.key.get_pressed()
		moveplayer(person,keys,setting,ball)
		clock.tick(FPS)
		if time.time() - start_time > 120:  # 120초가 지나면 Q-테이블 저장 및 게임 재시작
			agent.save_q_table('q_table.pkl')
			main()
			return
		
		if game_start(start_time):
			global current_holder 
			check_wall(ball)
			for event in pygame.event.get(): #게임 종료 및 q_table 저장
				if event.type == pygame.QUIT:
					agent.save_q_table('q_table.pkl')
					pygame.quit()
					sys.exit()

			for person in hometeam + awayteam:      #모든플레이어 조회 해서 action 할당 및 state업데이트
				state = agent.get_state(environment)        #위치를 불러온다 (state 획득)
				action = agent.choose_action(state)         #할 행동을 고른다
				if action == 'move_up':     
					person.moveup()
				elif action == 'move_down':
					person.movedown()
				elif action == 'move_left':
					person.moveleft()
				elif action == 'move_right':
					person.moveright()              #플레이어가 움직이는 액션일 경우의 처리
				if person.ball_following:           #플레이어가 공을 잡고있을때
					if action == 'pass':            #플레이어가 패스
						teammates = [p for p in (hometeam if person in hometeam else awayteam) if p != person]  #공을 잡은 플레이어의 팀선수들 (공을 잡은 사람 제외) 
						if teammates:       
							target_player = random.choice(teammates)        #랜덤으로 패스받을 선수 선택
							person.pass1(ball, target_player)           #패스
							pass_in_progress = True
							pass_target_player = target_player
					elif action == 'search':           #액션이 search 일때 처리
						person.search()         #search 함수
					elif action == 'shoot':         #액션이 shoot일때
						x1 = 0
						x2 = 0
						y1 = 0
						y2 = 0                           

						if current_holder is not None:
							if current_holder.team == 'away':         #공을 잡고있는 선수가 away 팀일때 골대의 위치
								x1 = 18
								x2 = 111
								y1 = 354
								y2 = 657
							if current_holder.team == 'home':           #공을 잡고있는 선수가 home 팀일때 골대의 위치
								x1 = 1691
								x2 = 1786
								y1 = 354
								y2 = 657

							if abs(distance(current_holder.x, current_holder.y, (x1 + x2) / 2, (y1 + y2) / 2)) < 500:       #공을 잡은 플레이어와 목표 골대사이의 거리가 500보다 작을때
								current_holder.shoot1(ball, x1, x2, y1, y2)             #목표 골대로 슛
				else:
					if action == 'intercept':           #액션이 intercept 일때
						person.intercept(ball)          #인터셉트 함수
				
				reward = calculate_reward(action, environment)      #어떤 액션에 대한 보상
				next_state = agent.get_state(environment)           #액션 이후의 state 가져오기
				agent.learn(state, action, reward, next_state)      #학습


			if not any(player.ball_following for player in hometeam + awayteam): #가장 가까운 플레이어(양팀1명)를 공쪽으로 이동
				closest_home_player = min(hometeam, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
				closest_away_player = min(awayteam, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
				move_towards_ball(closest_home_player, ball, closest_home_player.speed)
				move_towards_ball(closest_away_player, ball, closest_away_player.speed)

			for i in hometeam + awayteam: #ball_following 상태변화 검사
				d = distance(i.x, i.y, ball.x, ball.y) 
				if 0 <= d < ball.radius + i.radius and ball.speed < 3:
					i.ball_following = True
					current_holder = i
				else:
					i.ball_following = False

			if ball_moving: #패스나 슛을 해서 공이 움직일때의 공 위치변화
				ball.x += math.cos(ball_angle) * ball.speed * -1
				ball.y += math.sin(ball_angle) * ball.speed * -1
				ball.speed *= 0.99
				if ball.speed < 0.2:
					ball_moving = False
			
			for i in awayteam + hometeam+[person]: #각도를 기반으로 따라가기
				if i.ball_following:
					ball.x = i.x + math.cos(ball_angle) * 12
					ball.y = i.y + math.sin(ball_angle) * 12

			screen.fill((48, 131, 43))
			lines()
			person.draw()
			for i in range(len(hometeam)):
				hometeam[i].draw()
				awayteam[i].draw()
			ball.draw(current_holder)
			pygame.draw.line(screen, (255, 255, 255), (0, 5), (30, 5), 10)
			screen.blit(scoretext, [173, 56])

			pygame.transform.flip(goalpost2, True, False)

			screen.blit(goalpost1, [1300, 285])
			screen.blit(goalpost2, [-373, 285])
			pygame.display.update()
		else:
			screen.fill((255,255,255))
			screen.blit(stop, [900,500])

class Ball(): #공
	def __init__(self,radius):
		self.x = 1100
		self.y = 505
		self.radius = radius
		self.speed = 0
	def draw(self,person):
		if person is not None and person.ball_following == True:
			dx = person.x - self.x
			dy = person.y - self.y
			pygame.draw.circle(screen,(0,0,0),(self.x+(2*dx),self.y+(2*dy)),self.radius)
		else:
			pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius)
	
class Person(): #선수
	def __init__(self,radius,x,y,team):
		self.x = x
		self.y = y
		self.radius = radius
		self.speed = 2
		self.team = team
		
		self.ball_following = False
	
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
		#print(self.x,self.y,closest_player.x,closest_player.y)
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
		
	def pass2(self,ball):
		if self.ball_following:
			global ball_moving
			self.ball_following = False
			ball_moving = True
			ball.speed = int(setting['bluepasspower']) * 0.8

	def pass1(self, ball, target_player):
		if self.ball_following:
			global ball_moving
			self.search()
			angle = calculate_angle(self.x, self.y, target_player.x, target_player.y)
			angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
			angle_difference = abs(angle - angle_ball)
			#print(angle, angle_ball, angle_difference)
			if angle_difference < 0.1:  # 0.1 라디안 이내의 차이를 허용
				print(f"패스 시도: {self.team} 팀의 선수가 {target_player.team} 팀의 선수에게 패스")
				self.ball_following = False
				ball_moving = True
				if current_holder in hometeam:
					ball.speed = int(setting['redpasspower']) * 0.8
				elif current_holder in awayteam:
					ball.speed = int(setting['bluepasspower']) * 0.8

			#self.power.firstpower = 0
			#self.power.power = 0
			#self.power.power_growing = False
	def shoot1(self, ball, x1, x2, y1, y2):
		print(x1,x2,y1,y2)
		if self.ball_following:
			global ball_moving
			angle = calculate_angle(self.x, self.y, (x1+x2)/2, (y1+y2)/2)
			angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
			angle_difference = abs(angle - angle_ball)
			#print(angle, angle_ball, angle_difference)
			if angle_difference < 0.2:  # 0.1 라디안 이내의 차이를 허용
				self.ball_following = False
				ball_moving = True
				if current_holder in hometeam:
					ball.speed = int(setting['redshootpower'])*1.05
				elif current_holder in awayteam:
					ball.speed = int(setting['bluepasspower'])*1.05
			#self.power.firstpower = 0
			#self.power.power = 0
			#self.power.power_growing = False

	def calculate_angle(x1, y1, x2, y2): 
		return math.atan2(y2 - y1, x2 - x1)

	def draw(self):
		if self.team == 'home':
			self.color = (255,0,0)
		if self.team == 'away':
			self.color = (0,0,255)
		pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

	def intercept(self, ball):
		#print(self.team)
		global current_holder
		if current_holder is not None:
			#print(current_holder.team)
			if (not self.ball_following)  and (current_holder is not None) and (self.team != current_holder.team):
				#print("move")
				move_towards_ball(self, ball, self.speed) 
				
if __name__ == '__main__':
	main()