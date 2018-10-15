import season
import pprint


season = season.Season()

#sal = season.all_fixtures()
#pprint.pprint(sal)

#pprint.pprint(sr)

#for round in range(1, season.number_of_rounds()+1):
#    print(f'Round {round}')
#    try:
#        games = season.games_for_round(round)
#    except ValueError as err:
#        print(err)
#    else:
#        for g in games:
#            print(f"{g['homeTeam']} {g['goalsHomeTeam']} - {g['goalsAwayTeam']} {g['awayTeam']}")

next_round = season.first_unstarted_round()

print(f'Round {next_round}')
try:
    games = season.games_for_round(next_round)
except ValueError as err:
    print(err)
else:
    for g in games:
        print(season.predict_result(g))
        