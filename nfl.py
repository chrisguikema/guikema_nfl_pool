#!/usr/bin/env python

import nflgame, nflgame.update_sched
import sys, csv, os
import json
import random, time

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

def print_sorted_scorecard(scorecard, week):
    season_dict = dict()
    week_dict = dict()

    for name in scorecard:
        score = 0
        for i in range(1, 18):
            score += scorecard[name]['week%d' % i]

        week_dict['%s' % name] = scorecard[name]['week%d' % week]
        season_dict['%s' % name] = score

    print "----------------------"
    print " 2017 Week %d Results" % week
    print "----------------------"
    for name, score in sorted(week_dict.items(), key=lambda p:p[1], reverse=True):
        print name, score

    print "---------------------"
    print " 2017 Season Results"
    print "---------------------"
    for name, score in sorted(season_dict.items(), key=lambda p:p[1], reverse=True):
        print name, score

    print "---------------------"

def get_schedule(week):
    home = []
    away = []
    schedule = nflgame.update_sched.week_schedule(2017, 'REG', week)
    for game in schedule:
        home.append(game.get('home'))
        away.append(game.get('away'))

    return home, away

def gen_random(week):
    names = ['Curt', 'Amy', 'Laura', 'Tyler', 'Katie', 'Troy', 'Chris', 'Sam']
    home, away = get_schedule(week)

    with open('%sWeek %d.csv' % (CSV_DIRECTORY, week), "rb") as guik_picks:
        rd = csv.reader(guik_picks)
        for row in rd:
            if row[1] in names:
                names.remove(row[1])

    if names is not None:
        with open('%sWeek %d.csv' % (CSV_DIRECTORY, week), "ab") as guik_picks:
            wr = csv.writer(guik_picks)
            now = time.strftime("%x") + " " + time.strftime("%X")
            for name in names:
                random_picks = ["\r" + now, name]
                for i in range(0, len(home)):
                    if random.getrandbits(1):
                        random_picks.append(home[i])
                    else:
                        random_picks.append(away[i])
                wr.writerow(random_picks)

def get_winners(week):

    # Note: run the following command if there are games that have been played, but
    #       this function isn't returing proper values
    #
    # sudo python /usr/local/lib/python2.7/dist-packages/nfldb/update.py
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
    gen_random(week)
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
        save_scorecard(scorecard)
        print_sorted_scorecard(scorecard, week)

if __name__ == "__main__":
    if len(sys.argv[1:]) > 1:
        print "Too Many Arguments!"
        exit(-1)
    inputted_week = int(sys.argv[1:][0])
    main(inputted_week)
