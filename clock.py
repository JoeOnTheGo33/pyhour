#!/usr/bin/env python3
from datetime import datetime
import pandas as pd
import os
path = os.path.dirname(__file__)

def read_log(log_path):
    return pd.read_csv(log_path, delimiter=',', quotechar='"')

if __name__ == "__main__":
    DIV = "-----  "
    log_path = "w4.hours"
    log = read_log(os.path.join(path, log_path))

    WORKING = log.iloc[-1,-1]
    print("> Opened log file [%s]" % log_path)
    print(log.tail())

    print()
    if WORKING != 0:
        print(DIV, "WORKING @", log.iloc[-1,-2])
    else:
        print(DIV, "IDLE @", log.iloc[-1,-2])

    new_log = []

    cmd = ""
    while True:
        cmd = input("\t\t\t::")

        ## Override Commands
        if cmd == "" or cmd.lower() == "q":
            quit()
        elif not cmd.isalnum() and " " not in cmd:
            quit()
        elif cmd.startswith("s"):
            print()
            if len(new_log) == 0:
                print("Saved Nothing.")
            else:
                with open(log_path, 'a') as f:
                    for l in new_log:
                        print("SAVED <<", *l)
                        f.write(",".join(l) + "\n")
                    new_log = []
            print()
            continue

        if cmd.endswith(" q") or cmd == "sq":
            quit()

        ## Command Processing
        x = cmd.split(" ")
        if len(x) > 1:
            W = x[0]
            S = " ".join(x[1:])

            if W != "2":
                S = S.upper()

            if W.lower() == "out":
                W = "0"
            elif W.lower() == "in":
                W = "1"

            now = datetime.now()
            t = now.strftime("%H:%M")

            new_log.append([now.strftime("%y/%m/%d"), t, S, W])

            if W == "1":
                print(t,"-", "WORKING @ %s" % S)
            elif W == "0":
                print(t,"-", "IDLE @ %s" % S)
