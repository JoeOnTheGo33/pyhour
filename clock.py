#!/usr/bin/env python3
from datetime import datetime
import pandas as pd

def read_log(log_path):
    return pd.read_csv(log_path, delimiter=',', quotechar='"')

if __name__ == "__main__":
    DIV = "-----  "
    log_path = "hours.log"
    log = read_log(log_path)

    WORKING = log.iloc[-1,-1]
    print("> Opened log file [%s]" % log_path)
    print(log.tail())

    print()
    if WORKING != 0:
        print(DIV, "WORKING")
    else:
        print(DIV, "IDLE")

    new_log = []

    quit()
    cmd = ""
    while True:
        cmd = input("\t\t\t::")

        if cmd == "" or cmd.lower() == "q":
            print("Nothing saved.")
            quit()
        elif not cmd.isalnum() and " " not in cmd:
            print("Nothing saved.")
            quit()
        elif cmd.startswith("s"):
            print()
            if len(new_log) == 0:
                print("Saved Nothing.")
            else:
                with open(log_path, 'a') as f:
                    for l in new_log:
                        print("SAVED", l)
                        f.write(",".join(l) + "\n")
                    new_log = []

            print()
            continue
        if cmd.endswith("q"):
            quit()

        x = cmd.split(" ")
        W = x[0]
        if W != "2":
            S = "_".join(x[1:])
            S = S.upper()
        else:
            S = " ".join(x[1:])
        if W.lower() == "out":
            W = "0"
        now = datetime.now()
        t = now.strftime("%H:%M")
        new_log.append([now.strftime("%y/%m/%d"), t,S,W])
        if W == "1":
            print(t,"-", "WORKING (%s)" % S)
        elif W == "0":
            print(t,"-", "IDLE (%s)" % S)
        elif W.lower() == "in":
            W = "1"
        now = datetime.now()
        t = now.strftime("%H:%M")
        new_log.append([now.strftime("%y/%m/%d"), t,S,W])
        if W == "1":
            print(t,"-", "WORKING (%s)" % S)
        elif W == "0":
            print(t,"-", "IDLE (%s)" % S)
