import pygame
import sys
import os
import random
import time
import math

screen_width = 800
screen_height = 600
tape_list = ['001', '002', '003', '004', '005', '006', '007', '008']
'''
tape_list = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010',
'011', '012', '013', '014', '015', '016', '017', '018', '019', '020',
'021', '022', '023', '024', '025', '026', '027', '028', '029', '030',
'031', '032', '033', '034', '035', '036', '037', '038', '039', '040',
'041', '042', '043', '044', '045', '046', '047', '048', '049', '050',
'051', '052', '053', '054', '055', '056', '057', '058', '059', '060',
'061', '062', '063', '064', '065', '066', '067', '068', '069', '070',
'071', '072', '073', '074', '075', '076', '077', '078', '079', '080',
'081', '082', '083', '084', '085', '086', '087', '088', '089', '090',
'091', '092', '093', '094', '095', '096', '097', '098', '099', '100']
'''
pygame.init()
fps = 60
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font('TektonPro-Bold.otf', 26)

current = 'START'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)

background_image = pygame.image.load('background.png').convert()
background = pygame.Surface((background_image.get_width(), background_image.get_height()), pygame.SRCALPHA)
background.fill((0, 0, 0, 0,))
background.blit(background_image, (0,0))

start_button = pygame.Rect(400-150//2, 300-50//2, 150, 50)
start_textb = font.render('Start', True, BLACK)
start_textw = font.render('Start', True, WHITE)

initial = True

def AAfilledRoundedRect(surface,rect,color,radius=0.4):
    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

while True:
    #get all the keys being pressed
    pressed_keys = pygame.key.get_pressed()

    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:  # If user clicks 'X' button
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:  # If user has a key pressed down
            alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]  # Left 'ALT' or Right 'ALT' key
            if event.key == pygame.K_ESCAPE:  # If user pressed 'ESCAPE' key
                quit_attempt = True
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True

        if quit_attempt:
            pygame.quit()
            sys.exit()
        else:
            filtered_events.append(event)

    # GAME START
    screen.blit(background, (0, 0))

    if current == 'START':
        if start_button.collidepoint(pygame.mouse.get_pos()):
            AAfilledRoundedRect(screen,start_button,BLACK,0.5)
            screen.blit(start_textw, (400 - start_textw.get_width() // 2, 300 - start_textw.get_height() // 2))
            for event in filtered_events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    current = 'GAME'
        else:
            AAfilledRoundedRect(screen,start_button,WHITE,0.5)
            screen.blit(start_textb, (400 - start_textb.get_width() // 2, 300 - start_textb.get_height() // 2))

    if current == 'GAME':
        if initial:
            pygame.time.delay(3000)
            length = math.ceil(pygame.mixer.Sound('tapes/000_1.ogg').get_length() * 1000)
            pygame.mixer.music.load('tapes/000_1.ogg')
            pygame.mixer.music.play(1)
            pygame.time.delay(length)
            initial = False

        if len(tape_list) > 0:
            card = random.choice(tape_list)
            print(card)
            tape_list.remove(card)
        else:
            current = 'FINISH'
        
        current_card = 'cards/' + card + '.png'
        current_tape1 = 'tapes/' + card + '_1.ogg'
        current_tape2 = 'tapes/' + card + '_2.ogg'
        
        cardImg = pygame.image.load(current_card).convert()
        cardImg = pygame.transform.scale(cardImg, (313, 437))
        screen.blit(cardImg, (200 - cardImg.get_width() // 2, 300 - cardImg.get_height() // 2))
        length1 = math.ceil(pygame.mixer.Sound(current_tape1).get_length() * 1000)
        length2 = math.ceil(pygame.mixer.Sound(current_tape2).get_length() * 1000)

        pygame.mixer.music.load(current_tape1)
        pygame.mixer.music.play(1)
        pygame.time.delay(length1)
        pygame.time.delay(5000)
        pygame.mixer.music.load(current_tape2)
        pygame.mixer.music.play(1)
        pygame.time.delay(length2)
        pygame.time.delay(2500)


    pygame.display.flip() #update the screen
    clock.tick(fps)
