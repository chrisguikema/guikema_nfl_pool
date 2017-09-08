#!/usr/bin/env python

import nflgame
import sys, csv, pdb


def main():
    home = []
    away = []
    schedule = nflgame._search_schedule(year=2017, week=1)
    for game in schedule:
        home.append(game.get('home'))
        away.append(game.get('away'))

    with open('Week 1.csv', "ab") as nfl_sched:
        wr = csv.writer(nfl_sched)
        wr.writerow(home)
        wr.writerow(away)

if __name__ == "__main__":
    main()
