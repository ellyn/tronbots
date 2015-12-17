
#cython: profile=True
from constants import *
from collections import deque
import numpy as np
from scipy.sparse import lil_matrix
import sys
sys.setrecursionlimit(2000)
import timeit

def get_safe_directions(player1, player2):
    possible_directions = range(4)
    safe_directions = possible_directions[:]
    head = player1.segments[0].topleft
    # Prevent collisions with board edges and players
    for direction in possible_directions:
        delta = DIRECTION_DELTAS[direction]
        x = head[0] + delta['x'] * CELL_WIDTH
        y = head[1] + delta['y'] * CELL_WIDTH
        possible_head = Rect(x, y, CELL_WIDTH, CELL_WIDTH)
        if player1.has_collided(player2, head=possible_head):
            safe_directions.remove(direction)

    return safe_directions

def simple_ratio_heuristic(player, opponent):
    player_safe_count = len(get_safe_directions(player, opponent))
    opponent_safe_count = len(get_safe_directions(opponent, player))
    if player_safe_count == 0:
        return LOSE
    if opponent_safe_count == 0:
        return WIN
    return (player_safe_count - opponent_safe_count) / 3.0

def get_state(player, opponent):
    state = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    for rect in player.segments:
        loc = rect.topleft
        x,y = loc[0]/CELL_WIDTH, loc[1]/CELL_WIDTH
        state[y,x] = FRIENDLY
    for rect in opponent.segments:
        loc = rect.topleft
        x,y = loc[0]/CELL_WIDTH, loc[1]/CELL_WIDTH
        state[y,x] = OPPONENT
    return state

def manhattan_distance(a,b):
    x1,y1 = a
    x2,y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

cdef inline grid_neighbors(int row, int col):
    if ((0 < row < GAME_ROWS-1) and 0 < col < GAME_COLS-1):
      return [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
    l = []
    if (row+1 < GAME_ROWS):
        l += [(row+1, col)]
    if (row > 0):
        l += [(row-1, col)]
    if (col+1 < GAME_COLS):
        l += [(row, col+1)]
    if (col > 0):
        l += [(row, col-1)]
    return l

cdef inline dijkstra(state, head):
    hc,hr = head[0]/CELL_WIDTH, head[1]/CELL_WIDTH
    dists = np.zeros((GAME_ROWS, GAME_COLS), dtype=np.float)
    dists[:] = np.inf
    visited = np.zeros((GAME_ROWS, GAME_COLS), dtype=np.int)
    dists[hr,hc] = 0.0
    q = grid_neighbors(hr,hc)
    qfst = np.zeros(GAME_TILES+1, dtype=np.int)
    qsnd = np.zeros(GAME_TILES+1, dtype=np.int)
    cdef int qw = 0
    cdef int qc = 0
    for n in grid_neighbors(hr,hc):
        r,c = n
        dists[r,c] = 1
        qfst[qw] = r
        qsnd[qw] = c
        qw += 1
    cdef int qi = 0
    cdef int cr = 0
    cdef int cc = 0
    cdef int ndist = 0
    cdef int nr = 0
    cdef int nc = 0
    while qw != qi:
        cr = qfst[qi]
        cc = qsnd[qi]
        qi += 1
        ndist = dists[cr,cc] + 1
        for n in grid_neighbors(cr,cc):
            nr = n[0]
            nc = n[1]
            if state[nr,nc] != 0:
                continue
            if ndist < dists[nr,nc]:
                dists[nr,nc] = ndist
            if visited[nr,nc] == 0:
                qfst[qw] = nr
                qsnd[qw] = nc
                qw += 1
                visited[nr,nc] = 1
    return dists

cdef float compute_voronoi(player, opponent,state):
    #start_time = timeit.default_timer()
    head = player.segments[0].topleft
    ophead = opponent.segments[0].topleft
    player_costs = dijkstra(state, head)
    op_costs = dijkstra(state, ophead)
    cdef int pcount = 0
    cdef int opcount = 0
    cdef int maxcost = GAME_ROWS + GAME_COLS
    for r in xrange(GAME_ROWS):
        for c in xrange(GAME_COLS):
            if player_costs[r,c] < op_costs[r,c] and player_costs[r,c] <= maxcost:
                pcount += 1
            elif op_costs[r,c] < player_costs[r,c] and op_costs[r,c] <= maxcost:
                opcount += 1
    return float(pcount - opcount) / GAME_TILES
    #cdef float v = float(pcount - opcount) / GAME_TILES
    #print str(timeit.default_timer() - start_time)
    #return v

def voronoi_heuristic(player,opponent):
    state = get_state(player, opponent)
    return compute_voronoi(player,opponent,state)

cdef inline id_mat(r,c):
    return r*GAME_HEIGHT/CELL_WIDTH + c

def hopcroft_tarjan(state):
    parents = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    parents[:] = np.inf
    parents[0,0] = -1
    visited = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    low = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    low[:] = np.inf
    depths = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    depths[:] = np.inf
    rec_hopcroft_tarjan(state, 0, 0, 0, depths, parents, visited, low)

def rec_hopcroft_tarjan(state, row, col, depth, depths, parents, visited, low):
    visited[row, col] = 1
    depths[row,col] = depth
    low[row,col] = depth
    children = 0
    for n in grid_neighbors(row,col):
        nr,nc = n
        if state[nr,nc] != 0 and state[nr,nc] != ARTICULATION:
            continue
        if visited[nr,nc] == 0:
            parents[nr,nc] = id_mat(row,col)
            rec_hopcroft_tarjan(state, nr, nc, depth+1, depths, parents, visited, low)
            children += 1
            if (low[nr,nc] >= depths[row,col]) and (parents[row,col] != -1):
                state[row,col] = ARTICULATION
            low[row,col] = min(low[row,col], low[nr,nc])
        elif id_mat(nr,nc) != parents[row,col]:
            low[row,col] = min(low[row,col], depths[nr,nc])
    if (parents[row,col] == -1 and children >= 2):
        state[row,col] = ARTICULATION

def chamber_heuristic(player,opponent):
    state = get_state(player,opponent)
    hopcroft_tarjan(state)
    return compute_voronoi(player, opponent, state)
