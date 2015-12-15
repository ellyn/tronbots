
from constants import *
import Queue


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
    #state = player.get_state(other_player)
    #head = player.segments[0].topleft
    #hx,hy = head[0]/CELL_WIDTH, head[1]/CELL_WIDTH
    #assert state[hy,hx] == FRIENDLY, "Head of player not friendly"
    player_safe_count = len(get_safe_directions(player, opponent))
    opponent_safe_count = len(get_safe_directions(opponent, player))
    if player_safe_count == 0:
        return LOSE
    if opponent_safe_count == 0:
        return WIN
    return (player_safe_count - opponent_safe_count) / 3.0

def get_state(self, other_player):
    state = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    for rect in self.segments:
        loc = rect.topleft
        x,y = loc[0]/CELL_WIDTH, loc[1]/CELL_WIDTH
        state[y,x] = FRIENDLY
    for rect in other_player.segments:
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
        if (col+1 < maxcol):
            l += [(row+1,col+1)]
        if (col-1 > 0):
            l += [(row+1,col-1)]
    if (row-1 > 0):
        if (col+1 < maxcol):
            l += [(row-1, col+1)]
        if (col-1 > 0):
            l += [(row-1, col-1)]
    return l

def dijkstra(state, head):
    hc,hr = head
    dists = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
    dists[:] = np.inf
    dists[hy,hx] = 0.0

    q = Queue.Queue()

    for n in grid_neighbors(hr,hc):
        q.put(n)

    while not q.empty():
        cr,cc = q.get()
        ndist = dists[cr,cc] + 1
        for n in grid_neighbors(cr,cc):
            nr,nc = n
            if (state[nr,nc] != 0):
                continue
            if (ndist < dists[nr,nc]):
                dists[nr,nc] = ndist
            q.push(n)

    return dists

def voronoi_heuristic(player,opponent):
    head = player.segments[0].topleft
    ophead = opponent.segments[0].topleft
    pc,pr = head[0]/CELL_WIDTH, head[1]/CELL_WIDTH
    ec,er = ophead[0]/CELL_WIDTH, ophead[1]/CELL_WIDTH
    state = get_state(player)
    player_costs = dijkstra(state, head)
    op_costs = dijkstra(state, ophead)
    pcount = 0
    opcount = 0
    for r in GAME_HEIGHT/CELL_WIDTH:
        for c in GAME_WIDTH/CELL_WIDTH:
            if player_costs[r,c] < op_costs[r,c]:
                pcount += 1
            if op_costs[r,c] < player_costs[r,c]:
                opcount += 1
    if opcount == 0:
        return WIN
    return (pcount - opcount) / float(pcount+opcount) 
