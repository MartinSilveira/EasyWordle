from sources.others.config import *

def write_to_stats(iterations, avg_attempts, wordles_solved, attempt_freq):
    with open(STATS_PATH, "w") as stats:
        stats.write(f"Number of Iterations:\n{iterations}\n")
        stats.write(f"\nAverage Attempts:\n{avg_attempts:.4f}\n")

        wordles_unsolved = iterations - wordles_solved
        wordle_solve_ratio = (wordles_solved/iterations) * 100
        stats.write(f"\nWordles Solved/Unsolved: ({wordle_solve_ratio:.2f}%)\n{wordles_solved}\n{wordles_unsolved}\n")

        stats.write("\nAttempts Frequency:\n")
        for a in range(N_ATTEMPTS):
            stats.write(f"{a + 1}: {attempt_freq[a]} ({((attempt_freq[a]/wordles_solved) * 100):.2f}%)\n")

def deleteLines(number_of_lines):
    for _ in range(number_of_lines):
        print("\033[F\033[2K", end="\r")