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
        elif STATE == REMATCH:
            rematch_options()
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
    GAMEVIEW.draw_startscreen()
    while True:
        if len(pygame.event.get(QUIT)) > 0:
            end_game()
        if (len(pygame.event.get(KEYDOWN)) != 0 or 
            len(pygame.event.get(MOUSEBUTTONDOWN)) != 0):
            break
    pygame.event.clear()
    STATE = PLAYER_SETTINGS

def player_settings():
    global STATE, P1_HUMAN
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
                game_ready, P1_HUMAN = GAMEVIEW.playersettings.handle_click(x,y)
                if game_ready:
                    STATE = GAME_SCREEN
                    return
        GAMEVIEW.draw_playersettings()
        FPSCLOCK.tick(FPS)

def play_match():
    global STATE, OUTCOME
    GAMEVIEW.setup_gamescreen()
    OUTCOME = IN_PROGRESS
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == KEYDOWN:
                if P1_HUMAN and event.key in KEY_DIRECTION:
                    GAMEVIEW.update_P1_direction(KEY_DIRECTION[event.key])
                elif event.key == K_ESCAPE:
                    end_game()
        OUTCOME = GAMEVIEW.check_game_status()
        if OUTCOME != IN_PROGRESS:
            STATE = REMATCH
            return
        GAMEVIEW.update_gamescreen()
        FPSCLOCK.tick(FPS)

def rematch_options():
    global STATE
    GAMEVIEW.draw_rematchoptions(OUTCOME)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
                next_state = GAMEVIEW.rematchoptions.handle_click(x,y)
                if next_state != -1:
                    STATE = next_state
                    return


if __name__ == '__main__':
    main()
