#!/usr/bin/env python3
from datetime import datetime
import pandas as pd
import argparse
import os

path = '/home/jy/Me/pyhour'


def parse_args():
    parser = argparse.ArgumentParser(description='Py Hour')
    parser.add_argument('m', nargs='?', help='0 - inactive | 1 - active', default=None)
    parser.add_argument('s', nargs='?', help='simple tag for time use', default=None)
    parser.add_argument('-l', help='list recent entries')
    args = parser.parse_args()
    return args

def read_log(log_path):
    return pd.read_csv(log_path, delimiter=',', quotechar='"')


def main():
    args = parse_args()
    m = args.m
    s = args.s
    DIV = "-----  "
    log_path = os.path.join(path, "w4.hours")
    log = read_log(log_path)

    WORKING = log.iloc[-1,-1]
    print("> Opened log file [%s]" % log_path)
    if m is None and s is None:
        print(log.tail())
        quit()

    print()

    if WORKING == 1:
        print(DIV, "ACTIVE   @", log.iloc[-1,-2])
    elif WORKING == 0:
        print(DIV, "INACTIVE @", log.iloc[-1, -2])
    else:
        print(DIV, "NOTE    //", repr(log.iloc[-1,-2]))

    ## Command Processing
    if s is None:
        if m == 1:
            s = "ONLINE"
        else:
            s = "OFFLINE"
    elif m != "2":
        s = s.upper().replace(" ", "_")

    now = datetime.now()
    t = now.strftime("%H:%m")

    print()
    entry = [now.strftime("%y/%m/%d"), t, s, m]
    with open(log_path, 'a') as f:
        f.write(",".join(entry) + "\n")

    if m == "1":
        print(t, "-", "ACTIVE   @", s)
    elif m == "0":
        print(t, "-", "INACTIVE @", s)
    elif m == "2":
        print(t, "-", "NOTE    //", repr(s))


if __name__ == "__main__":
    main()
