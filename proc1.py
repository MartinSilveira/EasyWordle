import sys

while True:
    command = sys.stdin.readline().strip()
    if command == "START":
        print("Process1")
        sys.stdout.flush()

 