import pygame, sys, os
from constants import *
from gameview import *

def main():
    initialize_game()
    while True:
        if STATE == START_SCREEN:
            start_screen()
        elif STATE == PLAYER_SETTINGS:
            player_settings()
        elif STATE == GAME_SCREEN:
            play_match()
        elif STATE == TRY_AGAIN:
            retry_options()
        elif STATE == END_GAME:
            end_game()
        else:
            raise Exception('Invalid game state')

def initialize_game():
    global GAMEVIEW, FPSCLOCK, STATE
    pygame.init()
    pygame.mixer.music.load('sounds' + os.sep + '572768_Section-B---Demo-2.mp3')
    pygame.mixer.music.play(-1)

    GAMEVIEW = GameView()
    FPSCLOCK = pygame.time.Clock()
    STATE = START_SCREEN

def end_game():
    pygame.quit()
    sys.exit()

def start_screen():
    global STATE
    GAMEVIEW.draw_start_screen()
    while True:
        if len(pygame.event.get(QUIT)) > 0:
            end_game()
        key_up = pygame.event.get(KEYUP)
        if key_up != [] and key_up[0].key == K_ESCAPE:
            end_game()
        if len(key_up) != 0:
            break
    pygame.event.get() # To clear the event queue
    STATE = PLAYER_SETTINGS

def player_settings():
    global STATE
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
                game_ready = GAMEVIEW.player_settings.handle_click(x,y)
                if game_ready:
                    STATE = GAME_SCREEN
                    return
        GAMEVIEW.draw_player_settings()
        FPSCLOCK.tick(FPS)

def play_match():
    global STATE
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitGame()
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    direction = UP
                elif event.key == K_LEFT or event.key == K_a:
                    direction = LEFT
                elif event.key == K_DOWN or event.key == K_s:
                    direction = DOWN
                elif event.key == K_RIGHT or event.key == K_d:
                    direction = RIGHT
                elif event.key == K_ESCAPE:
                    end_game()
        GAMEVIEW.draw_game_screen()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()