from utils.utils import clear_screen
from utils.utils import print_section
from utils.utils import SECTION_CHAR

SECTION_WIDTH = 0
OPTIONS_SORT_PLAYERS = ("z", "a", "b", "c", "d", "e", "f", "g", "h")
OPTIONS_SORT_TOURNAMENTS = ("z", "a", "b", "c", "d", "e", "f")


class ViewMenu:
    """This class represents a menu interface for a chess tournament management system.
    It provides various menu options for managing players, tournaments, and generating reports.
    """

    def menu_home():
        """ This method displays the home menu and returns the user's choice."""
        clear_screen()
        print_section("| Chess tournament Home menu |", SECTION_CHAR, SECTION_WIDTH)
        print("\n(1) - Player management")
        print("(2) - Tournament management")
        print("(3) - Reports")
        print("(q) - Quit")
        print("\nYour choice ? ")
        while True:
            user_answer = input(">> ").lower()
            if user_answer in ("1", "2", "3", "q"):
                break
            print("Please enter a valid option.")
        return user_answer

    def menu_player():
        """ This method displays the player menu and returns the user's choice. """
        print("(1) - Add players")
        print("(2) - Update players")
        print("(3) - Delete players")
        print("(4) - Import players")
        print("(q) - Back ...")
        print("\nYour choice ? ")
        while True:
            user_answer = input(">> ").lower()
            if user_answer in ("1", "2", "3", "4", "q") or OPTIONS_SORT_PLAYERS:
                break
            print("Please enter a valid option.")
        return user_answer

    def menu_tournament():
        """ This method displays the tournament menu and returns the user's choice."""
        print("(1) - Display or run a tournament")
        print("(2) - Add tournaments")
        print("(3) - Update tournaments")
        print("(4) - Delete tournaments")
        print("(q) - Back ...")
        print("\nYour choice ? ")
        while True:
            user_answer = input(">> ").lower()
            if user_answer in ("1", "2", "3", "4", "q") or OPTIONS_SORT_TOURNAMENTS:
                break
            print("Please enter a valid option.")
        return user_answer

    def menu_add_players_to_tournament(tournament_selected):
        """This method displays the menu for adding, removing players to a tournament,
        start the tournament and returns the user's choice."""
        print(
            f'Selected tournament : {tournament_selected["name"]}  '
            f'{tournament_selected["description"]}  '
            f'{tournament_selected["location"]}  '
            f'{tournament_selected["date_begin"]}  '
            f'{tournament_selected["status"]}  '
        )
        print(f'Selected player : {len(tournament_selected["players_list"])}\n')

        print_section("| Add players to a tournament |", SECTION_CHAR, 0)
        print("\n(1) - Change a tournament")
        print('(2) - Add or remove players to selected tournament with a "*" ')
        print('(3) - Remove all players with a "*" ')
        print("(4) - Start the tournament")
        print("(q) - Back ...")
        while True:
            user_answer = input("\nYour choice ? ").lower()
            if user_answer in ("1", "2", "3", "4", "q") or OPTIONS_SORT_PLAYERS:
                return user_answer
            else:
                print("Please enter a valid option.")

    def menu_add_scores():
        """This method displays the menu for adding scores, validate a round and returns the user's choice."""
        print_section("| Add scores |", SECTION_CHAR, 0)
        print("\n(1) - Add or modify scores")
        print("(2) - Round validation ")
        print("(q) - Back ...")
        while True:
            user_answer = input("\nYour choice ? ").lower()
            if user_answer in ("1", "2", "q"):
                return user_answer
            else:
                print("Please enter a valid option.")

    def menu_report():
        """ This method displays the report menu and returns the user's choice."""
        clear_screen()
        print_section("| Report menu |", SECTION_CHAR, SECTION_WIDTH)
        print("\n(1) - Display all players")
        print("(2) - Display all tournaments")
        print("(3) - Display summarize of a tournament")
        print("(4) - Display a tournament players")
        print("(5) - Display a tournament rounds and all round matches")
        print("(6) - Display all of a tournament")
        print("(q) - Back ...")
        print("\nYour choice ? ")
        while True:
            user_answer = input(">> ").lower()
            if user_answer in ("1", "2", "3", "4", "5", "6", "q"):
                break
            print("Please enter a valid option.")
        return user_answer

    def menu_select_tournament():
        """ This Method displays the menu for selecting a tournament and returns the user's choice."""
        print("(1) - Select a tournament")
        print("(q) - Back ...")
        print("\nYour choice ? ")
        while True:
            user_answer = input(">> ").lower()
            if user_answer in ("1", "q") or OPTIONS_SORT_TOURNAMENTS:
                break
            print("Please enter a valid option.")
        return user_answer

    def menu_back():
        """This method displays the menu for going back and returns the user's choice."""
        print("(q) - Back ...")
        print("\nYour choice ? ")
        while True:
            user_answer = input(">> ").lower()
            if user_answer == "q" or OPTIONS_SORT_TOURNAMENTS:
                break
            print("Please enter a valid option.")
        return user_answer

    def menu_quit():
        """This method displays the menu for quitting the program and returns the user's choice."""
        clear_screen()
        print_section("| Quit the Chess Tournament? |", SECTION_CHAR, SECTION_WIDTH)
        print("(y) - Yes")
        print("(n) - NO")
        print("\nYour choice ? ")
        user_answer = input(">> ")
        print()
        return user_answer
