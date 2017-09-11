#!/usr/bin/env python

import nflgame, nflgame.update_sched
import sys, csv, os
import json

CSV_DIRECTORY = 'csv/score/'
SCHED_DIRECTORY = 'csv/sched/'

def get_scorecard():
    scorecard = dict()

    if os.path.isfile('scorecard.json'):
        with open('scorecard.json', 'r') as results:
            scorecard = json.load(results)

    else:
        names = ['Curt', 'Amy', 'Laura', 'Tyler', 'Katie', 'Troy', 'Chris', 'Sam']
        for name in names:
            temp = { 'name': '%s' % name}
            for i in range(1, 18):
                temp.update({'week%d' % i: 0})
                scorecard['%s' % name] = temp

    return scorecard

def save_scorecard(scorecard):
    with open('scorecard.json', 'w') as f:
        json.dump(scorecard, f)

def calculate_score(week, scorecard):
    for name in scorecard:
        score = 0
        for i in range(1, 18):
            score += scorecard[name]['week%d' % i]
        print name, scorecard[name]['week%d' % week], score

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
    with open('%sWeek %d - sched.csv' % (SCHED_DIRECTORY, week), "wb") as nfl_sched:
        wr = csv.writer(nfl_sched)
        wr.writerow(away)
        wr.writerow(home)

def determine_correct_picks_and_update_scorecard(week, winners, scorecard):
    with open('%sWeek %d.csv' % (CSV_DIRECTORY, week), "rb") as guik_picks:
        rd = csv.reader(guik_picks)
        for row in rd:
            if row[1] in scorecard:
                scorecard[row[1]]['week%d' % week] = len(set(row) & set(winners))

    return scorecard

def main(week):
    if not os.path.isfile('%sWeek %d - sched.csv' % (SCHED_DIRECTORY, week)):
        print "Generating Schedule!"
        home, away = get_schedule(week)
        write_sched_csv(week, home, away)
    else:
        print "Calculating Score!"
        scorecard = determine_correct_picks_and_update_scorecard(week, get_winners(week), get_scorecard())
        calculate_score(week, scorecard)
        save_scorecard(scorecard)

if __name__ == "__main__":
    if len(sys.argv[1:]) > 1:
        print "Too Many Arguments!"
        exit(-1)
    inputted_week = int(sys.argv[1:][0])
    main(inputted_week)
