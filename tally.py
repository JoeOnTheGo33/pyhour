import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from datetime import datetime, timedelta
from datetime import date
from dateutil.rrule import rrule, DAILY
import dateutil.relativedelta as rel
import io

REQ = """Date,Required
2022-02-21,0
2022-02-22,0
"""
HOURS_PER_DAY = 7


def nice(v):
    if v < 0:
        return ("-%d:%02.0f" % (int(abs(v)), int((abs(v) % 1) * 60))).rjust(6)
    else:
        return ("%d:%02.0f" % (int(abs(v)), int((abs(v) % 1) * 60))).rjust(6)


if __name__ == "__main__":
    WEEK = datetime.today().isocalendar()[1]
    print(" " * 12 + "===", "WEEK", WEEK, "===")
    log = pd.read_csv("/home/jy/Me/pyhour/w4.hours", delimiter=',',
                      quotechar='"', parse_dates=[['Date', 'Time']],
                      date_parser=lambda x, y: pd.to_datetime(x + " " + y, format='%y/%m/%d %H:%M'))
    print("RECENT LOG:"); print(log.tail())
    tally = pd.DataFrame(columns=["Date", "Hours"])

    start = log.iloc[0]["Date_Time"]
    mode = log.iloc[0]["Mode"]
    h = 0.0

    print()
    print("  Start at:", start)
    print()

    for i, r in log.iloc[1:, :].iterrows():
        end = r["Date_Time"]
        mode2 = r["Mode"]

        if mode == 1:
            h += (end - start) / timedelta(hours=1)

        if end.date() > start.date():
            tally = pd.concat([tally, pd.DataFrame({"Date": [start.date()], "Hours": [h]})],
                              ignore_index=True, axis=0)
            h = 0.0

        start = r["Date_Time"]
        if mode2 == 0 or mode2 == 1:
            mode = mode2

    if mode == 1 and datetime.now() > start:
        h += (datetime.now() - start) / timedelta(hours=1)

    tally = pd.concat([tally, pd.DataFrame({"Date": [start.date()], "Hours": [h]})],
                      ignore_index=True, axis=0)

    tally["Date"] = pd.to_datetime(tally["Date"])

    req_override = pd.read_csv(
        io.StringIO(REQ),
        sep=",",
        parse_dates=['Date'])
    res = pd.merge(tally, req_override, on="Date", how="outer")
    res.loc[~res["Required"].notna(), "Required"] = HOURS_PER_DAY
    res["Required"] = pd.to_numeric(res["Required"])
    res.loc[~res["Hours"].notna(), "Hours"] = 0
    res["Hours"] = pd.to_numeric(res["Hours"])
    tally = res

    tally["Week"] = tally["Date"].apply(lambda x: x.isocalendar()[1])
    tally = tally.sort_values("Date")

    print("RECENT TALLY:")
    overtime = tally.loc[tally["Hours"] > 10]
    if overtime.shape[0] > 0:
        print("    OVERTIME ERROR !!")
        print(overtime)
        quit()
    print(tally.tail())
    tally.to_csv("tally.log", index=False)

    weekly_tally = tally.groupby("Week").sum()
    overtime = weekly_tally["Required"] > 35
    weekly_tally.loc[overtime, "Required"] = HOURS_PER_DAY * 5

    H = 0
    if date.today().weekday() != 4:
        rd = rel.relativedelta(days=1, weekday=rel.FR)
        next_friday = date.today() + rd
        print()
        print("Days left in week:")
        for dt in rrule(DAILY, dtstart=date.today() + timedelta(days=1), until=next_friday):
            H += HOURS_PER_DAY
            print(dt.strftime("\t%Y-%m-%d"))
        weekly_tally.at[weekly_tally.shape[0], "Required"] += H
    else:
        print()
        print("Happy Friday!")

    weekly_tally["Diff"] = weekly_tally["Required"] - weekly_tally["Hours"]

    print(); print("WEEKLY TALLY:"); print(weekly_tally.tail())

    HD = weekly_tally["Diff"].sum()

    print()
    print("RECENT:")
    print("    ", "This week: ".ljust(10), nice(weekly_tally.iloc[-1]["Diff"]), "    ",
          "Today: ".ljust(7), nice(tally.iloc[-1]["Required"] - tally.iloc[-1]["Hours"]),
          sep="")
    print("ACCUMULATED:")
    print("    ", "This week: ".ljust(10), nice(HD), "    ",
          "Today: ".ljust(7), nice(HD - H),
          sep="")
