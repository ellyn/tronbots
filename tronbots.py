import pygame, sys, os
from constants import *
from gameview import *
import math
import timeit

def main():
    initialize_game()
    while True:
        if STATE == START_SCREEN:
            start_screen()
        elif STATE == MODE_SELECT:
            mode_select()
        elif STATE == PLAYER_SETTINGS:
            player_settings()
        elif STATE == GAME_SCREEN:
            play_match()
        elif STATE == REMATCH:
            rematch_options()
        elif STATE == END_GAME:
            end_game()
        elif STATE == TOURNAMENT:
            tournament()
        elif STATE == TOURN_RESULTS:
            tournament_results()
        else:
            print STATE
            raise Exception('Invalid game state')

def initialize_game():
    global GAMEVIEW, FPSCLOCK, STATE
    pygame.init()
    pygame.mixer.music.load('sounds' + os.sep + 'theme.ogg')
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
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                pygame.event.clear()
                STATE = MODE_SELECT
                return


def player_settings():
    global STATE, P1_HUMAN
    GAMEVIEW.playersettings.reset()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
                game_ready = GAMEVIEW.playersettings.handle_click(x,y)
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
                if GAMEVIEW.is_p1_human() and event.key in KEY_DIRECTION:
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
            elif event.type == KEYDOWN and event.key == K_RETURN:
                STATE = GAME_SCREEN
                return

def mode_select():
    global STATE
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
                next_state = GAMEVIEW.modeselect.handle_click(x,y)
                if next_state != -1:
                    STATE = next_state
                    return
        GAMEVIEW.draw_modeselection()
        FPSCLOCK.tick(FPS)

AUTO_MODE = True
def str_of_bot(bot):
    s = ''
    alg = bot['algorithm']
    if (alg == HUMAN):
        s += 'HUMAN,N/A,N/A,N/A'
    if (alg == NAIVE):
        s += 'NAIVE,N/A,N/A,N/A'
    else:
        s += 'MINIMAX,'
        if (bot['pruning']):
            s += 'T,'
        else:
            s += 'F,'
        s += str(bot['depth']) + ','
        if bot['heuristic'] == SIMPLE_RATIO:
            s += 'RATIO'
        if bot['heuristic'] == VORONOI:
            s += 'VORONOI'
        if bot['heuristic'] == CHAMBER:
            s += 'CHAMBER'
    return s

def mean(l):
    s = reduce(lambda acc,v: acc + v, l)
    return s/float(len(l))

def pop_stdev(l):
    m = mean(l)
    devs = [(x - m)**2 for x in l]
    var = mean(devs)
    return math.sqrt(var)

def str_of_results(results):
    s = ''
    for metric in results:
        s += str(mean(metric)) + ',' + str(pop_stdev(metric)) + ','
    return s[:len(s)-1]

def str_of_bots_results(results,bots):
    p1w = results[0][0]
    p2w = results[0][1]
    p1t = str_of_results(results[3:4])
    p2t = str_of_results(results[4:])
    rem_results = str_of_results(results[1:3])
    p1 = str_of_bot(bots[0])
    p2 = str_of_bot(bots[1])
    return p1+','+str(p1w)+','+p1t+','+p2+','+str(p2w)+','+p2t+','+rem_results

def generate_csv():
    #player = [(b,h,)
    num_matches = 1
    algs = [NAIVE, MINIMAX]
    prunes = [True, False]
    depths = [1,2]
    heur = [SIMPLE_RATIO, VORONOI, CHAMBER]

    p1s = [{'algorithm':MINIMAX,'pruning':p,'depth':d,'heuristic':h}
        for p in prunes for d in depths for h in heur]
    p1s += [{'algorithm':NAIVE}]
    p2s = [{'algorithm':MINIMAX,'pruning':p,'depth':d,'heuristic':h}
        for p in prunes for d in depths for h in heur]
    p2s += [{'algorithm':NAIVE}]

    f = open("full_tournament_results.csv", 'a')
    f.write("Bot #1 Type,Pruning,Depth,Heuristic,Wins,Mean Turn Time,\
    Stdev Turn Time,Bot #2 Type,Pruning,Depth,Heuristic,Wins,Mean Turn Time, Stdev Turn Time,\
    Mean # Turns/Match,Stdev # Rounds/Match,Mean Sec/Match, Stdev Sec/Match\n")
    f.close()
    i = 0
    for p1 in p1s:
        for p2 in p2s:
            i += 1
            print "TOURNAMENT: " + str(i) + " of " + str(len(p1s))*len(p2s))
            results = play_tournament([p1,p2,num_matches], False)
            f = open("full_tournament_results.csv", 'a')
            f.write(str_of_bots_results(results,[p1,p2])+'\n')
            f.close()



def play_tournament(bot_info, write_results=True):
    global STATE
    num_matches = bot_info[2]
    game_screen = GameScreen()
    f = None
    matchrounds = []
    matchtimes = []
    p1times = []
    p2times = []
    if (write_results):
        f = open("tournament_results.csv", 'a')
        f.write("Bot #1 Type,Pruning,Depth,Heuristic,Wins,Mean Turn Time,\
        Stdev Turn Time,Bot #2 Type,Pruning,Depth,Heuristic,Wins,Mean Turn Time, Stdev Turn Time,")
        f.write("Mean # Turns/Match,Stdev # Rounds/Match,Mean Sec/Match, Stdev Sec/Match\n")
    for i in range(num_matches):
        print "match: " + str(i+1) + " of " + str(num_matches) + "..."
        matchround = 1
        game_screen.setup_game(bot_info[:2])
        outcome = game_screen.play_turn()
        matchtime = timeit.default_timer()
        while outcome == IN_PROGRESS:
            matchround += 1
            cturn_start = timeit.default_timer()
            outcome = game_screen.play_turn()
            if game_screen.is_player1_turn:
                p1times += [timeit.default_timer() - cturn_start]
            else:
                p2times += [timeit.default_timer() - cturn_start]
        matchrounds += [matchround]
        matchtimes += [timeit.default_timer() - matchtime]
    score = game_screen.get_results()
    results = [score,matchrounds,matchtimes,p1times,p2times]
    if (write_results):
        f.write(str_of_bots_results(results,bot_info[:2])+'\n')
        f.close()
    GAMEVIEW.draw_tournament_results(score)
    STATE = TOURN_RESULTS
    return results

def tournament():
    global STATE
    GAMEVIEW.tournament.reset()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos[0], event.pos[1]
                bot_info = GAMEVIEW.tournament.handle_click(x,y)
                if bot_info != None:
                    GAMEVIEW.draw_tournament()
                    if AUTO_MODE:
                        generate_csv()
                    else:
                        play_tournament(bot_info)
                    return
        GAMEVIEW.draw_tournament()
        FPSCLOCK.tick(FPS)

def tournament_results():
    global STATE
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end_game()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                pygame.event.clear()
                STATE = MODE_SELECT
                return



if __name__ == '__main__':
    main()
