# -------------------- IMPORTS --------------------
import pygame
import sys
import os
import random
import time
import math

# -------------------- PYGAME VARIABLE SETUP --------------------
FPS = 60
window_width = 800
window_height = 600

# -------------------- COLOURS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)

# -------------------- VARIABLES --------------------
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

# -------------------- SCENE BASE --------------------


class SceneBase:  # Base template for all scenes
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):  # This method will receive all the events that happened since the last frame
        print("uh-oh, you didn't override this in the child class")

    def Update(self):  # Put your game logic in here for the scene
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):  # Put your render code here. It will receive the main screen Surface as input
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):  # Function to switch to another scene
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)

# -------------------- SCENE BASE TEMPLATE --------------------

'''
class XScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            pass

    def Update(self):
        pass

    def Render(self, screen):
        pass
'''

# -------------------- FUNCTIONS --------------------


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

# -------------------- MAIN CODE --------------------


def run_game(width, height, fps, starting_scene):
    global font, background
    pygame.init()
    pygame.display.set_caption('Karuta Speaker')

    font = pygame.font.Font('TektonPro-Bold.otf', 26)

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    background_image = pygame.image.load('background.png').convert()
    background = pygame.Surface((background_image.get_width(), background_image.get_height()), pygame.SRCALPHA)
    background.fill((0, 0, 0, 0,))
    background.blit(background_image, (0,0))

    while active_scene is not None:

        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)

# -------------------- SCENES --------------------

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.start_hover = False
        self.start_button = pygame.Rect(400-150//2, 300-50//2, 150, 50)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if self.start_button.collidepoint(pygame.mouse.get_pos()):
                self.start_hover = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.SwitchToScene(KarutaScene())
            else:
                self.start_hover = False

    def Update(self):
        self.start_textb = font.render('Start', True, BLACK)
        self.start_textw = font.render('Start', True, WHITE)

    def Render(self, screen):
        screen.blit(background, (0, 0))

        if self.start_hover:
            AAfilledRoundedRect(screen,self.start_button,BLACK,0.5)
            screen.blit(self.start_textw, (400 - self.start_textw.get_width() // 2, 300 - self.start_textw.get_height() // 2))
        else:
            AAfilledRoundedRect(screen,self.start_button,WHITE,0.5)
            screen.blit(self.start_textb, (400 - self.start_textb.get_width() // 2, 300 - self.start_textb.get_height() // 2))

class KarutaScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

run_game(window_width, window_height, FPS, TitleScene())
pygame.quit()
sys.exit()