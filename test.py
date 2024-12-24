from sources.others.config import *
import numpy as np

words = np.array(["example"] * 10000, dtype="U10")

for iter in range(10000000):
    print(iter)
    # Append operation (efficient in Python lists)
    words_list = words.tolist()

    words_list.append("newword")

    # Copy operation
    words = np.array(words_list, dtype="U10")
    new_words = words.copy()

#outside loop 5000 iterations 0m0.189s

#inside loop 50000 iterations 10m17s
#outside loop 50000 iterations 1.600s
#around 1m3s decrease each 5000 iterations

#novos dados
#inside 1000 - 0m9.777s
#inside 10000 - 1m37.872s

#outside 10000 - 0m14.497s multiprocessing simple
#outside 10000 - 0.473s multiprocessing complex

