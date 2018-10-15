import season

season = season.Season()

next_round = season.first_unstarted_round()

print(f'Round {next_round}')
try:
    games = season.games_for_round(next_round)
except ValueError as err:
    print(err)
else:
    for game in games:
        print(season.predict_result(game))
        