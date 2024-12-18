import sys

while True:
    command = sys.stdin.readline().strip()
    if command == "START":
        print("Process2")
        sys.stdout.flush()

