import random
from utils.utils import serializations
from models.matches_model import Match
from models.tournaments_model import Tournament
from views.game_view import ViewGame
from views.tournaments_view import ViewTournament
from views.player_view import ViewPlayer
from controllers.tournament_controller import ControllerTournament
from controllers.player_controller import ControllerPlayer
from controllers.report_controller import ControllerReport


class ControllerGame:
    """This controller runs the game of tournament"""

    def __init__(self) -> None:
        self.tournament = Tournament()

    def __call__(self):
        pass

    def select_tournament(self):
        """Request a tournament and update the tournament instance."""
        tournament_selected = ViewTournament.select_tournament(
            ControllerTournament.tournaments_list
        )
        self.tournament.__dict__.update(tournament_selected)

    def add_or_remove_players(self):
        """Request a list of players and add or remove them from the tournament."""
        players_list_selected = ViewPlayer.select_players_to_add(
            ControllerPlayer.players_list
        )
        if players_list_selected:
            self.tournament.add_or_remove_players(players_list_selected)

    def remove_all_players(self):
        """Remove all players from the tournament"""
        self.tournament.remove_all_players()

    def start_tournament(self):
        """Depending on the conditions, start the tournament with the first round"""
        # need list of players not empty
        if not self.tournament.players_list:
            ViewGame.display_message("Please add your first players with option (2)")
            return
        # need list of players in even number
        is_even = len(self.tournament.players_list) % 2 == 0
        if not is_even:
            ViewGame.display_message(
                "Please add your players in even number - with option (2)"
            )
            return
        # need minimum nomber of player and round !
        if len(self.tournament.players_list) <= int(self.tournament.rounds_max):
            ViewGame.display_message(
                "The number of players must exceed the predetermined number of rounds, add more players"
            )
            return
        # add the first_round
        self.tournament.add_first_round()
        # Display reports
        ControllerReport.display_tournament_all(self)

    def display_last_round(self):
        """Displays matches of the last round"""
        ControllerReport.display_last_round(self.tournament)

    def add_scores(self):
        """Selects a match and updates the scores"""
        matches = serializations(self.tournament.get_matches()[-1])
        match_selected = ViewGame.select_match(matches)
        match_to_update = ViewGame.update_score_match(match_selected)
        match_ = Match()
        match_.__dict__.update(match_to_update)
        match_.save_update_record()

    def round_validation(self):
        """Check that all scores have been entered and closed the rounds or tournament."""
        if self.is_scores_not_done():
            ViewGame.display_message("Please, enter all matches scores")
            return
        if self.tournament.round_actual == self.tournament.rounds_max:
            self.tournament.round_closure()
            self.tournament.tournament_closure()
            ControllerReport.display_tournament_all(self)
        else:
            self.tournament.round_closure()
            self.build_matches()
            self.tournament.add_next_round()
            ControllerReport.display_tournament_all(self)

    def is_scores_not_done(self):
        """Check that all scores have been entered"""
        for match in self.tournament.get_matches()[-1]:
            if bool(match.score_A == "0" and match.score_B == "0"):
                return True

    def build_matches(self):
        """Builds unique matches based on the players results for the next round."""
        # Get a list of tuple of (player_id, scores) sorted by scores.
        players_score = self.get_players_score()
        # Draw groups of player with same score and update the players_list.
        self.draw_players(players_score)
        # avoid duplicate matches in the players_list.
        self.find_unique_matches()
        # draw to find the first player of each match.
        self.draw_white_or_black()
        # Alert if players will have duplicate matches.
        for i in range(0, len(self.tournament.players_list), 2):
            if self.is_matches_duplicate(self.tournament.players_list[i: i + 2]):
                print(
                    self.tournament.players_list[i: i + 2],
                    ": those players will have duplicate matches.",
                )
                input("Press key to exit the pause")

    def get_players_score(self):
        """Return a list of tuples ordered by scores of all players' id and their total score."""
        players_score = []
        for player_id in self.tournament.players_list:
            score = 0
            for match in self.tournament.get_matches_score():
                for item in match:
                    if item[0] == player_id:
                        score = score + float(item[1])
            players_score.append((player_id, score))
        # Ranking players following scores of the tournament.
        players_score = sorted(players_score, key=lambda x: x[1], reverse=True)
        return players_score

    def draw_players(self, players_score):
        """Draw of players with the same scores and update player_list."""
        players_list = []
        list_to_draw = []
        for i, item in enumerate(players_score, 0):
            # condition to compare current item score with next item score
            if i + 1 < len(players_score) and item[1] == players_score[i + 1][1]:
                list_to_draw.append(item[0])
                continue
            # Add the last player ID and random player IDs that have the same score
            if list_to_draw:
                list_to_draw.append(item[0])
                random.shuffle(list_to_draw)
                players_list.extend(list_to_draw)
                list_to_draw = []
            else:
                players_list.append(item[0])
        self.tournament.players_list = players_list

    def find_unique_matches(self):
        """avoids duplicates pair players by replacing them with the best candidates."""
        self.matches_list = self.tournament.get_matches_ids_chess()
        players_list = self.tournament.players_list

        for i in range(0, len(players_list), 2):
            player_A = players_list[i]
            player_B = players_list[i + 1]
            # condition to deal with last pair of player
            if i == len(players_list) - 2:
                # continue with reversed extended list
                tmp_list = players_list[-3::-1]
                players_list = players_list + tmp_list
            for j in range(i + 2, len(players_list)):
                if not self.is_matches_duplicate(players_list[i: i + 2]):
                    break
                next_candidate = players_list[j]
                players_list.remove(player_A)
                players_list.remove(next_candidate)
                players_list.insert(i, player_A)
                players_list.insert(i + 1, next_candidate)

                if not self.is_matches_duplicate(players_list[i: i + 2]):
                    break
                players_list.remove(player_B)
                players_list.remove(next_candidate)
                players_list.insert(i, player_B)
                players_list.insert(i + 1, next_candidate)

        players_list = players_list[0: len(self.tournament.players_list)]
        self.tournament.players_list = players_list

    def is_matches_duplicate(self, pair_players):
        """Checks if the pair of players (id_chess) have already played together"""
        # Check if [a, b] or [b, a] exist in matches_list
        for i in range(0, len(self.matches_list), 2):
            pair_matches = self.matches_list[i: i + 2]
            if pair_players == pair_matches or pair_players[::-1] == pair_matches:
                return True

    def draw_white_or_black(self):
        """White or black draw for each match in players_list"""
        new_list = []
        for i in range(0, len(self.tournament.players_list), 2):
            pair_to_draw = self.tournament.players_list[i: i + 2]
            random.shuffle(pair_to_draw)
            new_list.extend(pair_to_draw)
        self.tournament.players_list = new_list
        self.tournament.update_record()
