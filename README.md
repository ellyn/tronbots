# tronbots

TRONBOTS is an implementation of the two-player variant of the classic arcade game TRON, built with Python 2.7 with pygame 1.9.1. For a faster variant of the game, there is also the same game in Cython, which can be found under the cython folder. The game includes bots that use the popular Minimax algorithm with alpha-beta pruning, combined with various heuristic functions. You can choose to play against a bot or have two bots play against each other. A human player can control the character with either the arrow keys or the WASD keyboard buttons.

TRONBOTS is designed with a clean, minimal interface. All fonts and media used are freely distributed and can be found below.

To play the game, just run tronbots.py. To play the Cython version (recommended if you want real-time play with the more advanced bots), navigate the Cython folder first,  setup the Cython files, and run from there.

## Implemented Bots:
- Naive Bot (Only changes direction if the next turn will result in an immediate collision)
- Minimax Bot with Ratio Heuristic (Maximizes likelihood of closing off opponent)
- Minimax Bot with Voronoi Heuristic (Tries to maximizes the player's Voronoi region)
- Minimax Bot with Chamber Heuristic (uses the Chamber of Trees heuristic that improves upon Voronoi)

### Media Sources:
- Music: Section B - Demo 2 by steampianist (http://www.newgrounds.com/audio/listen/572768)
- Font: Montserrat (https://www.google.com/fonts/specimen/Montserrat)
