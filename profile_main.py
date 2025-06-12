import cProfile
import pstats
from main import main

cProfile.run('main()', 'profile_main.prof')

# Для зручності: показати топ-20 повільних функцій
stats = pstats.Stats('profile_main.prof')
stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)
