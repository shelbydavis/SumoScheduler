import argparse
import random

class Team(object):
    def __init__(self, name, cooldown=0, matches=0) :
        self.name = name
        self.cooldown = cooldown
        self.matches = matches

    def __str__(self):
        return "Team: %s Cooldown %s Matches %s" % (self.name, self.cooldown, self.matches)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cooldown", "-c", default=2, type=int)
    parser.add_argument("--matches", "-m", default=4, type=int)
    parser.add_argument("--tables", "-t", default=2, type=int)
    parser.add_argument("--teams")
    args = parser.parse_args()

    # Read in our list of teams
    teams = []
    with open(args.teams,'r') as team_file:
        for line in team_file:
            team_name = line.strip()
            t = Team(team_name, 0, 0)
            teams.append(t)

    # Generate all possible pairings
    all_pairs = [(t0,t1) for (i,t0) in enumerate(teams) for t1 in teams[i+1:]]
    random.shuffle(all_pairs)

    match_round = 0
    matches = []
    # Generate matches
    while len([t for t in teams if t.matches != args.matches]) > 1 :
        valid_matches = []
        # Choose some matches from teams that haven't competed recently
        for (t0,t1) in all_pairs :
            if t0.matches != args.matches and t1.matches != args.matches and t0.cooldown == 0 and t1.cooldown == 0 :
                if [(m0,m1) for (m0,m1) in valid_matches if m0 == t0 or m0 == t1 or m1 == t0 or m1 == t1] == []:
                    valid_matches.append((t0,t1))
            if len(valid_matches) == args.tables :
                break
           
        # Remove the chosen pairings from the available matches
        for m in valid_matches :
            all_pairs.remove(m)

        #update the cooldown counters
        for t in teams :
            if t.cooldown > 0 :
                t.cooldown = t.cooldown - 1
               
        #update the match and cooldown counters for these pairings
        match_teams = [t0 for (t0,t1) in valid_matches] + [t1 for (t0,t1) in valid_matches]
        for t in match_teams :
            t.cooldown = args.cooldown
            t.matches = t.matches + 1

        print "Round %s" % (match_round + 1)
        match_round = match_round + 1
        for (i,(t0,t1)) in enumerate(valid_matches) :
            print "\tTable %s: %s vs. %s" % ((i+1), t0.name, t1.name)
        matches.append(valid_matches)

    for t in teams:
        if t.matches != args.matches :
            print "Team %s only played %s times!" % (t.name, t.matches)
