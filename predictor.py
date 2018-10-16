import season

season = season.Season()

# next_round = season.first_unstarted_round()
round = 2

print(f'Round {round}')
try:
    games = season.games_for_round(round)
except ValueError as err:
    print(err)
else:
    for game in games:
        print(season.predict_result(game, round))
        