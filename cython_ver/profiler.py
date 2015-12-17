import pstats, cProfile

import tronbots

cProfile.runctx("tronbots.main()", globals(), locals(), "Profile1.prof")
pstats.Stats("Profile1.prof").strip_dirs().sort_stats("time").print_stats()
