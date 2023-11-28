import time
import random
from datetime import datetime
from models.database_model import DBChess
from models.database_model import db_tournament
from models.players_model import Player
from models.rounds_model import Round
from models.matches_model import Match

db_tournament = DBChess(db_tournament, "tournament")

player = Player()
match = Match()
round_ = Round()


class Tournament:
    """This class represents a model of tournament."""

    def __init__(
        self,
        name="",
        description="",
        location="",
        date_begin="",
        date_end="",
        round_actual="0",  # à effacer ?
        rounds_max="4",
        status="",
        rounds_list=[],
        players_list=[],
        id="",
    ):
        self.name = name                    # The name of the tournament.
        self.description = description      # The description of the tournament.
        self.location = location            # The location of the tournament.
        self.date_begin = date_begin        # The start date of the tournament.
        self.date_end = date_end            # The end date of the tournament.
        self.round_actual = round_actual    # The current round number of the tournament.
        self.rounds_max = rounds_max        # The maximum number of rounds in the tournament.
        self.status = status                # The status of the tournament (not started, started, ended).
        self.rounds_list = rounds_list      # The list of round IDs in the tournament.
        self.players_list = players_list    # The list of player IDs in the tournament.
        self.id = id                        # The ID of the tournament.
        self.doc_id = ""                    # The document ID in the database (not stored in the database).

    def save_record(self):
        """Saves the tournament attributes to the database."""
        delattr(self, "doc_id")
        db_tournament.save_record(self.__dict__)

    def update_record(self):
        """Updates the tournament attributes in the database."""
        doc_id_ = self.doc_id
        delattr(self, "doc_id")
        db_tournament.update_record_by_doc_id(self.__dict__, doc_id_)
        self.doc_id = doc_id_

    def load_records(self):
        """Loads all tournaments from the database and returns a list of tournament objects."""
        tournaments_object = []
        for record in db_tournament.load_records():
            tournament = Tournament()
            tournament.__dict__.update(record)
            tournament.doc_id = record.doc_id
            tournaments_object.append(tournament)
        return tournaments_object

    def delete_record(self):
        """Deletes the tournament record from the database."""
        db_tournament.delete_record_by_doc_id(self.doc_id)

    def add_or_remove_players(self, players_list):
        """Adds or removes players from the tournament based on the provided list of player IDs."""

        for player in players_list:
            id_chess = player["id"]
            if id_chess not in self.players_list:
                self.players_list.append(id_chess)
            else:
                self.players_list.remove(id_chess)
        self.update_record()

    def remove_all_players(self):
        """Removes all players from the tournament."""
        self.players_list = []
        self.update_record()

    def add_first_round(self):
        """AAdds the first round to the tournament."""
        self.status = "started"
        random.shuffle(self.players_list)  # random the players_list
        self.add_round()
        self.add_matches()

    def add_next_round(self):
        """Adds the next round to the tournament."""
        self.add_round()
        self.add_matches()

    def add_round(self):
        """Sets up a new round and saves it to the database."""
        # Generate a new unique id
        unique_id = str(time.time()).replace(".", "")
        self.rounds_list.append(unique_id)
        # update round_actual attribute of tournament
        self.round_actual = str(len(self.rounds_list))
        # set attributes of the new round
        round_.round_name = "round" + str(self.round_actual)
        round_.status = "started"
        round_.datetime_begin = datetime.now().strftime("%Y-%m-%d %H:%M")
        round_.list_match = []
        round_.id = unique_id
        # Save the new round in the database with the unique id and update the tournament
        round_.save_record()
        self.update_record()

    def add_matches(self):
        """Adds matches to the current round based on the players list."""
        for i in range(0, len(self.players_list), 2):
            # Generate a new unique id and add it in the list_match attribute of current round
            unique_id = str(time.time()).replace(".", "")
            round_.list_match.append(unique_id)
            # set attributes of the new match
            match.id = unique_id
            match.id_chess_A = self.players_list[i]
            match.id_chess_B = self.players_list[i + 1]
            # update the round in the database and save the match
            round_.save_update_record()
            match.save_update_record()
            # pair = [([self.players_list[i], "0"]), ([self.players_list[i+1], "0"])]

    def round_closure(self):
        """Updates the attributes of the current round to mark it as ended."""
        last_round = self.get_rounds()[-1]
        last_round.datetime_end = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )  # set datetime_end in the previous round
        last_round.status = "ended"
        last_round.save_update_record()

    def tournament_closure(self):
        """Updates the attributes of the tournament to mark it as ended."""
        self.status = "ended"
        self.date_end = datetime.now().strftime("%Y-%m-%d")
        self.update_record()

    def get_players(self):
        """Gets players of the tournament -> list of player objects."""
        players = []
        player_all = player.load_all()
        for player_id in self.players_list:
            for player_ in player_all:
                if player_id == player_.id:
                    players.append(player_)
        return players

    def get_rounds(self):
        """Retrieves all rounds of the tournament as a list of round objects."""
        rounds = []
        for round_id in self.rounds_list:
            round_obj = Round()
            round_obj.load_by_id(round_id)
            rounds.append(round_obj)
        return rounds

    def get_matches(self):
        """Retrieves all matches of the tournament as a list of match objects grouped by rounds."""
        matches_list = []
        for round_obj in self.get_rounds():
            matches = []
            for match_id in round_obj.list_match:
                match_obj = Match()
                match_obj.load_by_id(match_id)
                matches.append(match_obj)
            matches_list.append(matches)
        return matches_list

    def get_matches_score(self):
        """Retrieves the scores of all matches in the tournament."""
        matches = []
        for round_obj in self.get_rounds():
            match_obj = Match()
            for match_id in round_obj.list_match:
                match_obj.load_by_id(match_id)
                matches.append(match_obj.match())
        return matches

    def get_matches_ids_chess(self):
        """Retrieves the IDs of all players participating in the matches."""
        ids_chess_list = []
        for match in self.get_matches_score():
            ids_chess_list.extend([match[0][0], match[1][0]])
        return ids_chess_list
