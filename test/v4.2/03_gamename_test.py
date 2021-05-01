import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("gamename.txt") as f:

    gamename = f.readline()
    print(gamename)
