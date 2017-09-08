#!/usr/bin/env python

import nflgame, nflgame.update_sched
import sys, csv, pdb

def get_scorecard():
    scorecard = dict()
    names = ['Curt', 'Amy', 'Laura', 'Tyler', 'Katie', 'Troy', 'Chris', 'Sam']
    for name in names:
        temp = { 'name': '%s' % name}
        for i in range(1, 18):
            temp.update({'week%d' % i: 0})
        scorecard['%s' % name] = temp
    return scorecard

def calculate_score(scorecard):
    # TODO: Use Winner Spreadsheet to compare "lists" to determine score
    #       len(set(a) & set(b)) is a possibility
    for name in scorecard:
        score = 0
        for i in range(1, 18):
            score += scorecard[name]['week%d' % i]
        print name, score

def get_schedule(week):
    home = []
    away = []
    schedule = nflgame.update_sched.week_schedule(2017, 'REG', week)
    for game in schedule:
        home.append(game.get('home'))
        away.append(game.get('away'))

    return home, away

def get_winners(week):
    winners = [None, None]
    games = nflgame.games(2017, week=week)
    for g in games:
        winners.append(g.winner)
    return winners

def write_sched_csv(week, home, away):
    with open('csv/Week %d - sched.csv' % week, "wb") as nfl_sched:
        wr = csv.writer(nfl_sched)
        wr.writerow(home)
        wr.writerow(away)

def append_winners_csv(week, winners):
    with open('csv/Week %d.csv' % week, "ab") as guik_picks:
        wr = csv.writer(guik_picks)
        wr.writerow([])
        wr.writerow(winners)

def main(week):
    scorecard = get_scorecard()
    home, away = get_schedule(week)
    write_sched_csv(week, home, away)
    winners = get_winners(week)
    append_winners_csv(week, winners)
    calculate_score(scorecard)

if __name__ == "__main__":
    inputted_week = int(sys.argv[1:][0])
    main(inputted_week)
