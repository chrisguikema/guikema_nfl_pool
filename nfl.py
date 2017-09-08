#!/usr/bin/env python

import nflgame
import sys, csv, pdb

def get_scorecard():
    scorecard = dict()
    names = ['Curt', 'Amy', 'Laura', 'Tyler', 'Katie', 'Troy', 'Chris', 'Sam']
    for name in names:
        temp = { 'name': '%s' % name}
        for i in range(1, 18):
            temp1 = {'week%d' % i: 0}
            temp.update(temp1)
        scorecard['%s' % name] = temp

def main():
    home = []
    away = []
    schedule = nflgame._search_schedule(year=2017, week=1)
    for game in schedule:
        home.append(game.get('home'))
        away.append(game.get('away'))

    with open('Week 1.csv', "wb") as nfl_sched:
        wr = csv.writer(nfl_sched)
        wr.writerow(home)
        wr.writerow(away)

if __name__ == "__main__":
    scorecard = get_scorecard()
    main()
