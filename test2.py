import multiprocessing

def exec_proc(proc_path):
    with open(proc_path, "r") as proc:
        exec(proc.read())

for iter in range(10000):
    print(iter + 1)

    process1 = multiprocessing.Process(target=exec_proc, args=("proc1.py",))
    process2 = multiprocessing.Process(target=exec_proc, args=("proc2.py",))

    process1.start()
    process2.start()

    process1.join()
    process2.join()


#inside loop 5000 iterations 1m3.395s
#outside loop 5000 iterations 0m0.189s

#inside loop 50000 iterations 10m17s
#outside loop 50000 iterations 1.600s
#around 1m3s decrease each 5000 iterations

#novos dados
#inside 1000 - 0m9.777s
#inside 10000 - 1m37.872s

#outside 10000 - 0m14.497s multiprocessing simple