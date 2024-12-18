from sources.others.config import *
from sources.others.functions import *

attempts_freq = [0] * N_ATTEMPTS
with open(STATS_PATH, "r") as stats_file:
    ignore = stats_file.readline()
    iterations = int(stats_file.readline().strip())

    for i in range(0, 2):
        ignore = stats_file.readline()

    avg_attempts = float(stats_file.readline().strip())

    ignore = stats_file.readline()

    solved_rate = float((stats_file.readline().strip())[26:31])
    wordles_solved = int(stats_file.readline().strip())

    for i in range(0, 3):
        ignore = stats_file.readline()

    for i in range(0, 6):
        attempts_freq[i] = int(((stats_file.readline())[3:]).split()[0])

#sum new stats to current stats
new_attempts_freq = [0] * N_ATTEMPTS
with open(NEW_STATS_PATH, "r") as stats_file:
    ignore = stats_file.readline()
    new_iterations = int(stats_file.readline().strip())

    for i in range(0, 2):
        ignore = stats_file.readline()

    new_avg_attempts = float(stats_file.readline().strip())

    ignore = stats_file.readline()

    new_solved_rate = float((stats_file.readline().strip())[26:31])
    new_wordles_solved = int(stats_file.readline().strip())

    for i in range(0, 3):
        ignore = stats_file.readline()

    for i in range(0, 6):
        new_attempts_freq[i] = int(((stats_file.readline())[3:]).split()[0])

avg_attempts = ((avg_attempts * iterations) + (new_avg_attempts * N_ITERATIONS)) / (iterations + N_ITERATIONS)
iterations += new_iterations
wordles_solved += new_wordles_solved
for i in range(0, 6):
    attempts_freq[i] += new_attempts_freq[i]

write_to_stats(iterations, avg_attempts, wordles_solved, attempts_freq)


