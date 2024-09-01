import pygame
import sys
import random
#import soccer1
import start1
#import playerset
import json

def load_setting():
    with open("settings.json", 'r') as file:
        config = json.load(file)
    return config



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

white = (255, 255, 255)
black = (0, 0, 0)
button_color = (0,0,0)
button_hover_color = (0,20,0)
button_width, button_height = 150, 50
pygame.init()
rect1 = pygame.Rect(0,0,500,1000)
rect2 = pygame.Rect(500,0,500,1000)
width, height = 1800, 1000
button_x, button_y = 80,500
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button2_x, button2_y = 760,500
button2_rect = pygame.Rect(button2_x, button2_y, button_width, button_height)
screen = pygame.display.set_mode((width, height))
# 폰트 설정
font = pygame.font.Font('HANGILE-TYPECONDENSED.TTF', 32)
clock = pygame.time.Clock()
bluepass = font.render('passpower  1~10',0,(255,255,255))
blueshoot = font.render('shootpower  1~10',0,(255,255,255))
redshoot = font.render('shootpower  1~10',0,(255,255,255))
redpass = font.render('passpower  1~10',0,(255,255,255))
bluerunspeed = font.render('speed  1~10',0,(255,255,255))
redrunspeed = font.render('speed  1~10',0,(255,255,255))
save = font.render('save settings',0,(255,255,255))
reset = font.render('reset',0,(255,255,255))
title = font.render('Settings',0,(255,255,255))
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(self.text, True, BLACK)
        self.active = False
    def set_text(self,text):
        self.text = text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active #1회 클릭시 활성화, 1회 더 클릭시 비활성화
            else:
                self.active = False

            if self.active:
                self.color = BLACK
            else:
                self.color = GRAY
            
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    print(ord(event.unicode))
                    if ord(event.unicode) >= 48 and ord(event.unicode) <= 57:
                         self.text += event.unicode
                     #unicode값: 내가 입력한 키 이야기 하는것.
                self.txt_surface = font.render(self.text, True, BLACK)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)



def draw_button():
    pygame.draw.rect(screen, (66,70,182), rect1)
    pygame.draw.rect(screen, (195,40,40), rect2)
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



def main(width,height):

    setting = load_setting()
    screen = pygame.display.set_mode((width, height))
    running = True
    input_box1 = InputBox(200, 100, 50, 32, setting['bluepasspower']) 
    input_box2 = InputBox(200,200,50,32, setting['blueshootpower'])
    input_box3 = InputBox(600, 100, 50, 32, setting['redshootpower'])
    input_box4 = InputBox(600,200,50,32, setting['redpasspower'])
    input_box5 = InputBox(600, 300, 50, 32, setting['redrunspeed'])
    input_box6 = InputBox(200,300,50,32, setting['bluerunspeed'])
    input_boxes = [input_box1,input_box2,input_box3,input_box4,input_box5,input_box6]

    while running:
        #print(soccer1.X)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button2_rect.collidepoint(event.pos):
                    setting['bluepasspower'] = input_box1.text
                    setting['blueshootpower'] = input_box2.text
                    setting['redpasspower'] = input_box3.text
                    setting['redshootpower'] = input_box4.text
                    setting['redrunspeed'] = input_box5.text
                    setting['bluerunspeed'] = input_box6.text
                    
                    
                    with open("settings.json", 'w') as file:
                        json.dump(setting, file, ensure_ascii=False, indent=4)
                if button2_rect.collidepoint(event.pos):
                    start1.main()
                        
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    input_box1.set_text("5")
                    input_box2.set_text("5")
                    input_box3.set_text("5")
                    input_box4.set_text("5")
                    input_box5.set_text("5")
                    input_box6.set_text("5")
                    setting['bluepasspower'] = "5"
                    setting['blueshootpower'] = "5"
                    setting['redpasspower'] = "5"
                    setting['redshootpower'] = "5"
                    setting['redrunspeed'] = "5"
                    setting['bluerunspeed'] = "5"
                            
                    with open("settings.json", 'w') as file:
                        json.dump(setting, file, ensure_ascii=False, indent=4)
                if button_rect.collidepoint(event.pos):
                    start1.main()
              
        for box in input_boxes:
            box.update()
        
        screen.fill((57,129,69))
        draw_button()  
        for box in input_boxes:
            box.draw(screen)
        
        
        screen.blit(bluepass,[30,100])
        screen.blit(blueshoot,[30,200])
        screen.blit(redshoot,[830,200])
        screen.blit(redpass,[830,100])
        screen.blit(bluerunspeed,[30,300])
        screen.blit(redrunspeed,[830,300])
        screen.blit(reset,[130,500])
        screen.blit(save,[780,500])
        screen.blit(title,[465,50])
        pygame.display.flip()
        clock.tick(30)
#한개만 더만들어서 red, blue 수치 기록 하는걸로.      

if __name__ == "__main__":
    main()
