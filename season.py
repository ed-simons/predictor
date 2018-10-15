
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

def goals_average(goals_for, goals_against):
    if not goals_for:
        raise ValueError(f"Goals for is empty")

    if not goals_against:
        raise ValueError(f"Goals against is empty")

    gf = (sum(goals_for)/len(goals_for))
    ga = (sum(goals_against)/len(goals_against))

    return round((gf + ga)/2)

class Season:
    def __init__(self):
        self._all_games = list(json.load(open('league.json'))['api']['fixtures'].values())   # /fixtures/league/{league_id}

    def all_games(self):
        """
        Returns information for all games; played, live or unplayed.
        """
        return self._all_games

    def number_of_rounds(self):
        """
        Gets the number of rounds that make up the season.
        """
        return len({fixture['round'] for fixture in self._all_games})

    def games_for_round(self, round):
        """
        Returns information for all games in the round.
        """
        if round == 0 or round > self.number_of_rounds():
            raise ValueError(f'"round" must be 1 to {self.number_of_rounds()} inclusive')

        return [{'homeTeam': game['homeTeam'], 
                 'awayTeam': game['awayTeam'],
                 'goalsHomeTeam': game['goalsHomeTeam'],
                 'goalsAwayTeam': game['goalsAwayTeam'],
                 'status': game['status']} for game in self._all_games if game['round'] == f"Premier League - {round}"]

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
            
    def predict_result(self, game):
        """
        Predicts the result of the game.
        """
        if game['status'] != 'Not Started':
            raise ValueError(f"{game['homeTeam']} v {game['awayTeam']} has already started")

        if game['goalsHomeTeam']:
            raise ValueError(f"Home teams goals is invalid for unstarted match")
        
        if game['goalsAwayTeam']:
            raise ValueError(f"Away teams goals is invalid for unstarted match")


        homeTeamGoalsFor = list()
        homeTeamGoalsAgainst = list()
        awayTeamGoalsFor = list()
        awayTeamGoalsAgainst = list()

        for round in range(1, self.first_unstarted_round()):
            for games in self.games_for_round(round):
                if games['homeTeam'] == game['homeTeam']:
                    homeTeamGoalsFor.append(int(games['goalsHomeTeam']))
                    homeTeamGoalsAgainst.append(int(games['goalsAwayTeam']))
                    
                if games['awayTeam'] == game['awayTeam']:
                    awayTeamGoalsFor.append(int(games['goalsAwayTeam']))
                    awayTeamGoalsAgainst.append(int(games['goalsHomeTeam']))

        homeTeamGoals = goals_average(homeTeamGoalsFor, awayTeamGoalsAgainst)
        awayTeamGoals = goals_average(homeTeamGoalsAgainst, awayTeamGoalsFor)
        
        return f"{game['homeTeam']} {homeTeamGoals} -  {awayTeamGoals} {game['awayTeam']}"
        




        

