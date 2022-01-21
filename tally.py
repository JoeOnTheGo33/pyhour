from clock import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from datetime import datetime, timedelta

if __name__ == "__main__":
    WEEK = datetime.today().isocalendar()[1]
    print("WEEK", WEEK)
    log = pd.read_csv("w4.hours", delimiter=',',
        quotechar='"', parse_dates=[['Date', 'Time']],
        date_parser=lambda x,y: pd.to_datetime(x + " " + y, format='%y/%m/%d %H:%M'))
    print(log.tail())
    tally = pd.DataFrame(columns=["Date", "Hours"])

    start = log.iloc[0]["Date_Time"]
    mode = log.iloc[0]["Mode"]
    h = 0.0

    print("Start at:", start)

    for i,r in log.iloc[1:,:].iterrows():
        end = r["Date_Time"]
        mode2 = r["Mode"]

        if mode == 1:
            h += (end - start) / timedelta(hours=1)

        if end.date() > start.date():
            tally = pd.concat([tally, pd.DataFrame({"Date":[start.date()], "Hours":[h]})],
                ignore_index = True, axis = 0)
            h = 0.0

        start = r["Date_Time"]
        if mode2 == 0 or mode2 == 1:
            mode = mode2

    tally = pd.concat([tally, pd.DataFrame({"Date":[start.date()], "Hours":[h]})],
        ignore_index = True, axis = 0)

    tally["Week"] = tally["Date"].apply(lambda x: x.isocalendar()[1])

    weekly_tally = tally.groupby("Week").sum()
    weekly_tally["Required"] = 40
    weekly_tally.at[1,"Required"] = 8 * 4
    weekly_tally["Diff"] = weekly_tally["Required"] - weekly_tally["Hours"]

    print(tally.tail())
    tally.to_csv("tally.log", index=False)
    print(weekly_tally.tail())
    print(weekly_tally["Diff"].sum())
