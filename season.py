
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

        return round((sum(goals)/len(goals))/2)

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

    def games_for_round(self, round):
        """
        Returns information for all games in the round.
        """
        if round == 0 or round > self.number_of_rounds():
            raise ValueError(f'"round" must be 1 to {self.number_of_rounds()} inclusive')

        return [
                    {
                        'homeTeam': game['homeTeam'], 
                        'awayTeam': game['awayTeam'],
                        'goalsHomeTeam': game['goalsHomeTeam'],
                        'goalsAwayTeam': game['goalsAwayTeam'],
                        'status': game['status']
                    } 
                    for game in self._all_games if game['round'] == round
                ]

    def all_games_unstarted(self, round):
        """
        Returns True if no games have been started for the round.
        """
        if round == 0 or round > self.number_of_rounds():
            raise ValueError(f'"round" must be 1 to {self.number_of_rounds()} inclusive')

        return all([game['status']=='Not Started' for game in self.games_for_round(round)])

    def first_unstarted_round(self):
        """
        Returns the earliest round with no games started.

        Note that during a typical round some games may have finished, some will be in progress and others not started.
        """
        for round in range(1, self.number_of_rounds()+1):
            if self.all_games_unstarted(round):
                return round 
            
    def predict_result(self, game, round):
        """
        Predicts the result of the game.
        """

        hgf = self.stats(game['homeTeam'], round)['homeTeamGoalsFor']
        hga = self.stats(game['homeTeam'], round)['homeTeamGoalsAgainst']
        agf = self.stats(game['awayTeam'], round)['awayTeamGoalsFor']
        aga = self.stats(game['awayTeam'], round)['awayTeamGoalsAgainst']

        homeTeamGoals = self.goals_average(hgf, aga)
        awayTeamGoals = self.goals_average(agf, hga)
        
        return f"{game['homeTeam']} {homeTeamGoals} - {awayTeamGoals} {game['awayTeam']}"
        
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

    def stats(self, team, round):
        """
        Returns all stats for team.
        """

        homeTeamGoalsFor = [int(game['goalsHomeTeam']) for game in self._all_games if game['round'] < round and game['homeTeam'] == team]
        homeTeamGoalsAgainst = [int(game['goalsAwayTeam']) for game in self._all_games if game['round'] < round and game['homeTeam'] == team]
        awayTeamGoalsFor = [int(game['goalsAwayTeam']) for game in self._all_games if game['round'] < round and game['awayTeam'] == team]
        awayTeamGoalsAgainst = [int(game['goalsHomeTeam']) for game in self._all_games if game['round'] < round  and game['awayTeam'] == team]

        return {
                    'homeTeamGoalsFor': homeTeamGoalsFor,
                    'homeTeamGoalsAgainst': homeTeamGoalsAgainst,
                    'awayTeamGoalsFor': awayTeamGoalsFor,
                    'awayTeamGoalsAgainst': awayTeamGoalsAgainst
                }



        

