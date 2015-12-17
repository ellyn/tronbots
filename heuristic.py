
from constants import *
from collections import deque
import numpy as np
from scipy.sparse import lil_matrix
import sys
sys.setrecursionlimit(2000)

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

def grid_neighbors(row,col):
    maxrow = GAME_HEIGHT/CELL_WIDTH
    maxcol = GAME_WIDTH/CELL_WIDTH
    l = []
    if (row+1 < maxrow):
        l += [(row+1, col)]
    if (row > 0):
        l += [(row-1, col)]
    if (col+1 < maxcol):
        l += [(row, col+1)]
    if (col > 0):
        l += [(row, col-1)]
    return l

#def gen_sparse_graph():#
#    numrows = GAME_HEIGHT/CELL_WIDTH
#    numcols = GAME_WIDTH/CELL_WIDTH
#    m = lil_matrix((numrows,numcols))
#    for r in range(1, numrows-1):
#        for c in range(1, numcols-1):
#            m[r,c] =

def dijkstra(state, head):
    hc,hr = head[0]/CELL_WIDTH, head[1]/CELL_WIDTH
    dists = np.zeros((GAME_ROWS, GAME_COLS))
    dists[:] = np.inf
    visited = np.zeros((GAME_ROWS, GAME_COLS))
    dists[hr,hc] = 0.0
    ns = grid_neighbors(hr,hc)
    for n in ns:
        r,c = n
        dists[r,c] = 1
    q = deque(grid_neighbors(hr,hc))

    while len(q) != 0:
        cr,cc = q.popleft()
        ndist = dists[cr,cc] + 1
        for n in grid_neighbors(cr,cc):
            nr,nc = n
            if (state[nr,nc] != 0):
                continue
            if ndist < dists[nr,nc]:
                dists[nr,nc] = ndist
            if visited[nr,nc] == 0:
                q.append(n)
                visited[nr,nc] = 1
    return dists

def compute_voronoi(player, opponent,state):
    head = player.segments[0].topleft
    ophead = opponent.segments[0].topleft
    player_costs = dijkstra(state, head)
    op_costs = dijkstra(state, ophead)
    pcount = 0
    opcount = 0
    maxcost = GAME_ROWS + GAME_COLS
    for r in range(GAME_ROWS):
        for c in range(GAME_COLS):
            if player_costs[r,c] < op_costs[r,c] and player_costs[r,c] <= maxcost:
                pcount += 1
            if op_costs[r,c] < player_costs[r,c] and op_costs[r,c] <= maxcost:
                opcount += 1

    v = (pcount - opcount) / float(GAME_WIDTH*GAME_HEIGHT/(CELL_WIDTH*CELL_WIDTH))
    #print "Heuristic val: " + str(v)
    return v

def voronoi_heuristic(player,opponent):
    state = get_state(player, opponent)
    return compute_voronoi(player,opponent,state)

def id_mat(r,c):
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
    #print 'visited: ' + str(visited)
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
