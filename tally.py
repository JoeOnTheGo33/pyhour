import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from datetime import datetime, timedelta
from datetime import date
from dateutil.rrule import rrule, DAILY
import dateutil.relativedelta as rel


def nice(v):
    return "%d:%02.0f" % (int(v), int((v % 1) * 60))


if __name__ == "__main__":
    WEEK = datetime.today().isocalendar()[1]
    print("WEEK", WEEK)
    log = pd.read_csv("/home/jy/Me/pyhour/w4.hours", delimiter=',',
                      quotechar='"', parse_dates=[['Date', 'Time']],
                      date_parser=lambda x, y: pd.to_datetime(x + " " + y, format='%y/%m/%d %H:%M'))
    print(log.tail())
    tally = pd.DataFrame(columns=["Date", "Hours"])

    start = log.iloc[0]["Date_Time"]
    mode = log.iloc[0]["Mode"]
    h = 0.0

    print()
    print("Start at:", start)

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

    tally = pd.concat([tally, pd.DataFrame({"Date": [start.date()], "Hours": [h]})],
                      ignore_index=True, axis=0)

    tally["Week"] = tally["Date"].apply(lambda x: x.isocalendar()[1])

    weekly_tally = tally.groupby("Week").sum()
    weekly_tally["Required"] = 35
    weekly_tally.at[1, "Required"] = 8 * 4
    weekly_tally["Diff"] = weekly_tally["Required"] - weekly_tally["Hours"]

    print()
    print(tally.tail())
    tally.to_csv("tally.log", index=False)
    print()
    print(weekly_tally.tail())

    H = 0
    rd = rel.relativedelta(days=1, weekday=rel.FR)
    next_friday = date.today() + rd
    print()
    print("Days left in week:")
    for dt in rrule(DAILY, dtstart=date.today() + timedelta(days=1), until=next_friday):
        H += 8
        print(dt.strftime("\t%Y-%m-%d"))

    HD = weekly_tally["Diff"].sum()

    print()
    print("RECENT:")
    print("\tHours required this week:\t", nice(weekly_tally.iloc[-1]["Diff"]))
    print("ACCUMLATED:")
    print("\tHours required this week:\t", nice(HD))
    print("\tHours required today:\t\t", nice(HD - H))

    input("...")
