import argparse
import random
from collections import deque

class Match(object) :
    def __init__(self, table, round_num, team_1, team_2) :
        self.table = table
        self.round_num = round_num
        self.team_1 = team_1
        self.team_2 = team_2

    def __str__(self) :
        return "Round %s table %s \"%s\" vs. \"%s\"" % (self.round_num, self.table, self.team_1.name, self.team_2.name)
    
class Team(object):
    def __init__(self, name) :
        self.name = name
        self.matches = []

    def last_match(self) :
        round_num = None
        for m in self.matches :
            if round_num == None or m.round_num > round_num :
                round_num = m.round_num
        return round_num
       
    def played_team(self, team) :
        played = False
        for m in self.matches :
            if team == m.team_1 or team == m.team_2 :
                played = True
        return played
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cooldown", "-c", default=2, type=int)
    parser.add_argument("--matches", "-m", default=4, type=int)
    parser.add_argument("--tables", "-t", default=2, type=int)
    parser.add_argument("--teams")
    args = parser.parse_args()

    while True :
        # Read in our list of teams
        teams = []
        with open(args.teams,'r') as team_file:
            for line in team_file:
                team_name = line.strip()
                t = Team(team_name)
                teams.append(t)

        # Generate all possible pairings
        all_pairs = [(t0,t1) for (i,t0) in enumerate(teams) for t1 in teams[i+1:]]
        played_pairs = []
        delayed_pairs = deque()
        random.shuffle(all_pairs)

        match_round = 0
        table = 0
        matches = []
        # Generate matches
        for (t0,t1) in all_pairs :
            # Teams haven't played all their matches
            if len(t0.matches) < args.matches and  len(t1.matches) < args.matches:
                # both teams have had enough time to rest 
                if (t0.last_match() == None or match_round - t0.last_match() >= args.cooldown) and \
                   (t1.last_match() == None or match_round - t1.last_match() >= args.cooldown) :
                    matches.append(Match(table, match_round, t0, t1))
                    t0.matches.append(matches[-1])
                    t1.matches.append(matches[-1])
                    played_pairs.append((t0,t1))
                    table = table + 1
                    if table >= args.tables :
                        table = 0
                        match_round = match_round + 1
                else :
                    delayed_pairs.append((t0,t1))

        # Clean up pass
        tick = 0
        while len([t for t in teams if len(t.matches) < args.matches]) > 1 and len(delayed_pairs) > tick:
            (t0,t1) = delayed_pairs.popleft()
            # Teams haven't played all their matches
            if len(t0.matches) < args.matches and  len(t1.matches) < args.matches:
                # both teams have had enough time to rest 
                if (t0.last_match() == None or match_round - t0.last_match() >= args.cooldown) and \
                   (t1.last_match() == None or match_round - t1.last_match() >= args.cooldown) :
                    matches.append(Match(table, match_round, t0, t1))
                    t0.matches.append(matches[-1])
                    t1.matches.append(matches[-1])
                    played_pairs.append((t0,t1))
                    table = table + 1
                    if table >= args.tables :
                        table = 0
                        match_round = match_round + 1
                    tick = 0
                else :
                    delayed_pairs.append((t0,t1))
                    tick = tick + 1

        if len([t for t in teams if len(t.matches) < args.matches]) == 0 :
            break
    
    for m in matches :
        print m
