import subprocess

# Start subprocesses
process1 = subprocess.Popen(["python3", "proc1.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
process2 = subprocess.Popen(["python3", "proc2.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

for i in range(1, 5000):
    print(f"Iteration {i}")

    # Signal the subprocesses to start their operation and get the outputs
    process1.stdin.write("START\n")
    process1.stdin.flush()
    process2.stdin.write("START\n")
    process2.stdin.flush()

    # Wait for responses from both subprocesses
    output1 = process1.stdout.readline().strip()
    output2 = process2.stdout.readline().strip()

    print(output1)
    print(output2)

#inside loop 5000 iterations 1m3.395s
#outside loop 5000 iterations 0m0.189s

#inside loop 50000 iterations 10m17s
#outside loop 50000 iterations 1.600s
#around 1m3s decrease each 5000 iterations