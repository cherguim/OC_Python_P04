from models.players_model import Player
from views.player_view import ViewPlayer

# A dictionary of options for sorting the players.
OPTIONS_PLAYERS = {
    "a": "sex",
    "b": "first_name",
    "c": "last_name",
    "d": "country_code",
    "e": "date_of_birth",
    "f": "rating",
    "g": "rank",
    "h": "id",
    "z": "",
}


class ControllerPlayer:
    """This class manages the registration of tournament players, display, sorting, deletion and updating."""

    options_sort = OPTIONS_PLAYERS  # A dictionary of options for sorting the players.
    sort_by = ""                    # The attribute to sort the players by.
    players_list = []               # A list of player dictionaries.

    def player_add():
        """Add a new player."""
        user_answers = ViewPlayer.add_player()
        player = Player(*user_answers)
        player.save()
        ViewPlayer.display_player_details(player.__dict__)
        user_answers = ViewPlayer.get_yes_or_no_add_another_player()
        if user_answers == "y":
            ControllerPlayer.player_add()

    def players_display(tournament=""):
        """Display the list of players."""
        ControllerPlayer.players_list = []
        player = Player()
        players_objects = player.load_all()
        for player in players_objects:
            ControllerPlayer.players_list.append(player.__dict__)
        if not ControllerPlayer.sort_by == "":
            ControllerPlayer.players_list.sort(
                key=lambda x: x[ControllerPlayer.sort_by]
            )
        file_name = ""
        ViewPlayer.display_players_list(
            ControllerPlayer.players_list, tournament, file_name
        )
        return

    def players_sort_by(user_answer):
        """Sort the players by a specific attribute."""
        if user_answer in OPTIONS_PLAYERS:
            sort_option = OPTIONS_PLAYERS[user_answer]
            ControllerPlayer.sort_by = sort_option
            ControllerPlayer.players_display()

    def player_delete():
        """"Delete players."""
        players_selected_to_delete = ViewPlayer.select_players_to_delete(
            ControllerPlayer.players_list
        )
        if players_selected_to_delete:
            player = Player()
            user_answers = ViewPlayer.get_yes_or_no_delete_players()
            if user_answers == "y":
                for player_list in players_selected_to_delete:
                    player.__dict__.update(player_list)
                    player.delete()
        return ControllerPlayer.players_display()

    def player_update():
        """Update player details."""
        players_selected_to_update = ViewPlayer.select_players_to_update(
            ControllerPlayer.players_list
        )
        if players_selected_to_update:
            player = Player()
            for i, player_list in enumerate(players_selected_to_update):
                player_updated = ViewPlayer.update_player(player_list)
                player.__dict__.update(player_updated)
                player.update()
                ViewPlayer.display_player_details(player.__dict__)
                if i != len(players_selected_to_update) - 1:
                    user_answers = ViewPlayer.get_yes_or_no_update_next_player()
                    if user_answers == "n":
                        break
                else:
                    ViewPlayer.get_continue()
        return ControllerPlayer.players_display()

    def player_import():
        """Import players from a file (not yet implemented)."""
        input("this function has not yet been implemented, press a key...")
