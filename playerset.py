import pygame
import math

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((500, 500))

# 색상 설정
white = (255, 255, 255)

# FPS 설정
clock = pygame.time.Clock()

# 원 클래스 정의
class CircleWithImage:
    def __init__(self, x, y, radius, image_path):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = pygame.image.load(image_path)  # 이미지 불러오기
        self.image = pygame.transform.scale(self.image, (self.radius , self.radius ))  # 원 크기에 맞게 이미지 크기 조정
        self.angle = 0  # 회전 각도 초기화

    def draw(self, surface):
        # 이미지를 중심을 기준으로 회전
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))  # 중심을 유지하면서 회전
        
        # 회전된 이미지 그리기
        surface.blit(rotated_image, rotated_rect.topleft)

    def rotate(self, angle_speed):
        # 각도 증가 (이미지 회전 속도)
        self.angle += angle_speed

# CircleWithImage 객체 생성 (이미지 경로는 적절히 설정)
circle_image = CircleWithImage(250, 250, 50, "your_image.png")  # your_image.png는 이미지 파일 경로로 교체

# 프로그램 실행 중인지 확인하는 변수
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경 색상
    screen.fill(white)

    # 이미지 회전시키기
    circle_image.rotate(1)  # 회전 속도 1도씩
    circle_image.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(60)

# Pygame 종료
pygame.quit()
