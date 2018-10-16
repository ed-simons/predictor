import season

def result_string(result):
        return f"{result['homeTeam']} {result['goalsHomeTeam']} - {result['goalsAwayTeam']} {result['awayTeam']}"

def calculate_wadzy_score(predicted, actual, joker):

    correct_goals = lambda t: goals_out(t) == 0
    goal_difference = lambda r: r['goalsHomeTeam'] - r['goalsAwayTeam']
    correct_goal_difference = lambda: goal_difference(predicted) == goal_difference(actual)
    result = lambda r: 0 if goal_difference(r) == 0 else (1 if goal_difference(r) > 0 else -1)
    correct_result = lambda: result(predicted) == result(actual)
    exact_scoreline = lambda: correct_goals('goalsHomeTeam') and correct_goals('goalsAwayTeam')
    goals_out = lambda t: abs(predicted[t] - actual[t])
    is_joker = lambda t: actual[t] == joker
    jokers_match = lambda: is_joker('homeTeam') or is_joker('awayTeam')

    score = 0
    if correct_goals('goalsHomeTeam'):
        score += 6 if is_joker('homeTeam') else 2
    if correct_goals('goalsAwayTeam'):
        score += 6 if is_joker('awayTeam') else 2
    if correct_goal_difference():
        score += 2 if jokers_match() else 1
    if correct_result():
        score += 12 if jokers_match() else 6
    if exact_scoreline():
        score += 18 if jokers_match() else 9
    score -= goals_out('goalsHomeTeam') * (2 if is_joker('homeTeam') else 1)
    score -= goals_out('goalsAwayTeam') * (2 if is_joker('awayTeam') else 1)
    return score

season = season.Season()

for r in range(1, season.first_unstarted_round()):
    print(f'Round {r}')
    try:
        games = season.games_for_round(r)
    except ValueError as err:
        print(err)
    else:
        for game in games:
            prediction = season.predict_result(game, r)
            actual = season.actual_result(game)

            print(f"Prediction: {result_string(prediction)}")
            print(f"Actual:     {result_string(actual)}")

            print(f"wadzy_score = {calculate_wadzy_score(prediction, actual, 'Arsenal')}")

        