import random
import csv


class Team:
    def _init_(self, name, rating, language):
        self.name = name
        self.rating = rating
        self.language = language
        self.score = 0
        self.match_times = []

    def update_rating(self, points, opponent_rating, win):
        if win:
            self.rating += 2 if self.rating > opponent_rating else 5
        else:
            self.rating -= 2 if self.rating > opponent_rating else 5
        self.score += points

    def _repr_(self) -> str:
        return f"{self.name}({self.rating}, {self.language}, {self.score})"


def simulate_match(team1, team2):
    # No matchup
    if team2 is None:
        team1.update_rating(1, team1.rating - 1, True)
        return

    noise1, noise2 = random.randint(-4, 4), random.randint(-4, 4)
    performance1, performance2 = team1.rating + noise1, team2.rating + noise2
    match_time = random.randint(5, 10)
    team1.match_times.append(match_time)
    team2.match_times.append(match_time)

    # Determine the winner based on the performance
    rating_diff = abs(performance1 - performance2)
    if rating_diff < 5:
        winner = team1 if random.random() < 0.5 else team2
    elif rating_diff < 10:
        winner = team1 if performance1 > performance2 else team2
        if random.random() > 0.65:
            winner = team2 if winner is team1 else team1
    else:
        winner = team1 if performance1 > performance2 else team2
        if random.random() > 0.90:
            winner = team2 if winner is team1 else team1

    # Update ratings and scores
    if winner is team1:
        team1.update_rating(1, team2.rating, True)
        team2.update_rating(0, team1.rating, False)
    else:
        team2.update_rating(1, team1.rating, True)
        team1.update_rating(0, team2.rating, False)


def pair_teams(teams):
    pairings = []
    for i in range(0, len(teams) - 1, 2):
        pairings.append((teams[i], teams[i + 1]))
    if len(teams) % 2 != 0:
        pairings.append((teams[-1], None))
    return pairings


# Load the teams data from the data.csv file
teams_by_lang = {}
with open("./data.csv", "r") as file:
    reader = csv.reader(file)
    reader = iter(reader)
    next(reader)  # skip the header row
    for row in reader:
        try:
            teams_by_lang[row[2]].append(Team(row[0], int(row[1]), row[2]))
        except KeyError:
            teams_by_lang[row[2]] = [Team(row[0], int(row[1]), row[2])]

# Simulate 10 rounds of the tournament
for lang, teams in teams_by_lang.items():
    for round in range(10):
        pairings = pair_teams(teams)
        for team1, team2 in pairings:
            simulate_match(team1, team2)

        # Sort teams based on score, rating, and total match time
        teams.sort(key=lambda x: (-x.score, -x.rating, sum(x.match_times)))

# Combine all teams into a single list
all_teams = []
for teams_by_lang in teams_by_lang.values():
    all_teams.extend(teams_by_lang)

# Sort teams based on score, rating, and total match time
all_teams.sort(key=lambda x: (-x.score, -x.rating, sum(x.match_times)))

# Display the final leaderboard
print("Name\tScore\tRating")
for team in all_teams:
    print(f"{team.name}\t{team.score}\t{team.rating}")