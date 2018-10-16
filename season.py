
import json

# These code snippets use an open-source library. http://unirest.io/python
# response = unirest.get("https://api-football-v1.p.mashape.com/fixtures/league/2",
#   headers={
#     "X-Mashape-Key": "373pmkisjSmshA8AnqLLWdONNgDPp1aejcgjsnoZZjd4yJPpHX",
#     "Accept": "application/json"
#   }
# )
# 
# Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
# Connection: keep-alive
# Content-Type: application/json
# Date: Thu, 16 Aug 2018 22:35:11 GMT
# Expires: Thu, 19 Nov 1981 08:52:00 GMT
# Pragma: no-cache
# Server: Mashape/5.0.6pwd

# Transfer-Encoding: chunked

class Season:
    def __init__(self):
        self._all_games = list(json.load(open('league.json'))['api']['fixtures'].values())   # /fixtures/league/{league_id}
        # Convert round strings to integers
        for game in self._all_games:
            game['round'] = int(game['round'][len('Premier League - '):])

    @staticmethod
    def goals_average(goals_for, opponents_goals_against):
        """
        Returns the average from two lists of goals.
        """
        goals = goals_for + opponents_goals_against
        if not goals:
            return 1

        return round(sum(goals)/len(goals))

    def all_games(self):
        """
        Returns information for all games; played, live or unplayed.
        """
        return self._all_games

    def number_of_rounds(self):
        """
        Gets the number of rounds that make up the season.
        """
        return len({game['round'] for game in self._all_games})

    def games_for_round(self, season_round):
        """
        Returns information for all games in the round.
        """
        if season_round == 0 or season_round > self.number_of_rounds():
            raise ValueError(f'"season_round" must be 1 to {self.number_of_rounds()} inclusive')

        return [
                    {
                        'homeTeam': game['homeTeam'], 
                        'awayTeam': game['awayTeam'],
                        'goalsHomeTeam': game['goalsHomeTeam'],
                        'goalsAwayTeam': game['goalsAwayTeam'],
                        'status': game['status']
                    } 
                    for game in self._all_games if game['round'] == season_round
                ]

    def all_games_unstarted(self, season_round):
        """
        Returns True if no games have been started for the round.
        """
        if season_round == 0 or season_round > self.number_of_rounds():
            raise ValueError(f'"season_round" must be 1 to {self.number_of_rounds()} inclusive')

        return all([game['status']=='Not Started' for game in self.games_for_round(season_round)])

    def first_unstarted_round(self):
        """
        Returns the earliest round with no games started.

        Note that during a typical round some games may have finished, some will be in progress and others not started.
        """
        for season_round in range(1, self.number_of_rounds()+1):
            if self.all_games_unstarted(season_round):
                return season_round 

    def predict_result(self, game, season_round):
        """
        Predicts the result of the game based on all games up to the given round.
        """

        hgf = self.stats(game['homeTeam'], season_round)['homeTeamGoalsFor']
        hga = self.stats(game['homeTeam'], season_round)['homeTeamGoalsAgainst']
        agf = self.stats(game['awayTeam'], season_round)['awayTeamGoalsFor']
        aga = self.stats(game['awayTeam'], season_round)['awayTeamGoalsAgainst']

        return {
                    'homeTeam': game['homeTeam'], 
                    'awayTeam': game['awayTeam'],
                    'goalsHomeTeam': self.goals_average(hgf, aga),
                    'goalsAwayTeam': self.goals_average(agf, hga)
                } 

    def actual_result(self, game):
        """
        Actual result of the game.
        """

        return {
                    'homeTeam': game['homeTeam'], 
                    'awayTeam': game['awayTeam'],
                    'goalsHomeTeam': int(game['goalsHomeTeam']),
                    'goalsAwayTeam': int(game['goalsAwayTeam'])
                } 

    def results(self, team):
        """
        Returns all results for team.
        """

        return [
                    {
                        'round': game['round'],
                        'homeTeam': game['homeTeam'], 
                        'awayTeam': game['awayTeam'],
                        'goalsHomeTeam': game['goalsHomeTeam'],
                        'goalsAwayTeam': game['goalsAwayTeam']
                    } 
                    for game in self._all_games if game['status'] == 'Match Finished' and (game['homeTeam'] == team or game['awayTeam'] == team)
                ]

    def stats(self, team, season_round):
        """
        Returns all stats for team.
        """
        return {
                    'homeTeamGoalsFor': [int(game['goalsHomeTeam']) for game in self._all_games if game['round'] < season_round and game['homeTeam'] == team],
                    'homeTeamGoalsAgainst': [int(game['goalsAwayTeam']) for game in self._all_games if game['round'] < season_round and game['homeTeam'] == team],
                    'awayTeamGoalsFor': [int(game['goalsAwayTeam']) for game in self._all_games if game['round'] < season_round and game['awayTeam'] == team],
                    'awayTeamGoalsAgainst': [int(game['goalsHomeTeam']) for game in self._all_games if game['round'] < season_round  and game['awayTeam'] == team]
                }



        

