from utils.utils import serializations
from views.reports_view import ViewReports


class ControllerReport:
    """This class is responsible for displaying various reports related to a tournament."""

    def __init__(self) -> None:
        pass

    def __call__(self):
        pass

    def display_last_round(tournament):
        """Displays the matches of the last round of a tournament."""
        ViewReports.clear_screen()
        round = serializations(tournament.get_rounds())
        ViewReports.display_round(round[-1])
        matches = serializations(tournament.get_matches()[-1])
        ViewReports.display_matches(matches)

    def display_tournament_summarize(tournament):
        """Displays the summary of a tournament."""
        tournament_dict = tournament.__dict__
        ViewReports.display_tournament_details(tournament_dict)

    def display_ranking(controllergame):
        """Displays the player rankings of a tournament."""
        if len(controllergame.tournament.rounds_list) > 1:
            players = controllergame.tournament.get_players()
            for player in players:
                score = [
                    str(item[1])
                    for item in controllergame.get_players_score()
                    if item[0] == player.id
                ][0]
                player.__dict__.update({"score": score})
            players_score = serializations(players)
            # Ranking players following scores of the tournament.
            players_score = sorted(players_score, key=lambda x: x['score'], reverse=True)
            ViewReports.display_ranking(players_score)

    def display_tournament_players(tournament):
        """Displays the players of a tournament."""
        ViewReports.clear_screen()
        players = serializations(tournament.get_players())
        ViewReports.display_tournament_players(players)

    def display_tournament_rounds_matches(tournament):
        """Displays the matches of each round in a tournament."""
        rounds = serializations(tournament.get_rounds())
        for i, round in enumerate(rounds):
            ViewReports.display_round(round)
            matches = serializations(tournament.get_matches()[i])
            ViewReports.display_matches(matches)

    def display_tournament_all(controllergame):
        """Displays all reports of a tournament."""
        tournament = controllergame.tournament
        ControllerReport.display_tournament_summarize(tournament)
        ControllerReport.display_ranking(controllergame)
        ControllerReport.display_tournament_rounds_matches(tournament)
        ViewReports.display_message()
