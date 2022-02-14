#!/usr/bin/env python3
from datetime import datetime
import pandas as pd
import argparse
import os

path = '/home/jy/Me/pyhour'


def parse_args():
    parser = argparse.ArgumentParser(description='Py Hour')
    parser.add_argument('m', nargs='?', choices=[0, 1], help='0 - inactive | 1 - active', default=None, type=int)
    parser.add_argument('s', nargs='*', help='simple tag for time use', default=None)
    parser.add_argument('-p', action='store_true', help='list recent entries')

    parser.add_argument('-l', action='store_true', help='go inactive for lunch')
    parser.add_argument('-x', action='store_true', help='go active status=ONLINE')
    parser.add_argument('-o', action='store_true', help='go inactive status=OFFLINE')
    parser.add_argument('-d', action='store_true', help='dry run')

    args = parser.parse_args()
    if args.l:
        args.m = 1
        args.s = "LUNCH"
    if args.x:
        args.m = 1
        args.s = "ONLINE"
    if args.o:
        args.m = 0
        args.s = "OFFLINE"
    if args.m is None and len(args.s) == 0:
        args.d = True
    if args.s is not None and isinstance(args.s, list):
        args.s = "_".join(args.s).upper()
    return args


def read_log(log_path):
    return pd.read_csv(log_path, delimiter=',', quotechar='"')


def main():
    args = parse_args()
    m = args.m
    s = args.s
    if args.d:
        print(args)
    log_path = os.path.join(path, "w4.hours")
    log = read_log(log_path)

    working = log.iloc[-1, -1]
    time = log.iloc[-1, 1]
    print("> Opened log file [%s]" % log_path)
    if args.p:
        print(log.tail())

    print()

    if working == 1:
        print(time, "- ACTIVE   @", log.iloc[-1, -2])
    elif working == 0:
        print(time, "- INACTIVE @", log.iloc[-1, -2])
    else:
        print(time, "- NOTE    //", repr(log.iloc[-1, -2]))

    # === Command Processing
    if s is None:
        if m == 1:
            s = "ONLINE"
        else:
            s = "OFFLINE"
    elif m != 2:
        s = s.upper().replace(" ", "_")

    now = datetime.now()
    t = now.strftime("%H:%M")

    print()
    entry = [now.strftime("%y/%m/%d"), t, s, str(m)]
    if not args.d:
        with open(log_path, 'a') as f:
            f.write(",".join(entry) + "\n")

    if m == 1:
        print(t, "- ACTIVE   @", s)
    elif m == 0:
        print(t, "- INACTIVE @", s)
    elif m == 2:
        print(t, "- NOTE    //", repr(s))


if __name__ == "__main__":
    main()
