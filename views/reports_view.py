from utils.utils import clear_screen
from utils.utils import print_section
from utils.utils import SECTION_CHAR

SECTION_WIDTH = 80


class ViewReports:
    """This class represents a menu interface for managing reports."""

    def display_tournament_details(tournament):
        """
        Displays the details of a tournament.

        Args:
        - tournament: A dictionary containing the details of the tournament.
        """

        clear_screen()
        print()
        print_section("| Tournament Details |", SECTION_CHAR, SECTION_WIDTH)
        print(f"\n{'Name':<15} {tournament.get('name', '')}")
        print(f"{'Description:':<15} {tournament.get('description', '')}")
        print(f"{'Location:':<15} {tournament.get('location', '')}")
        print(f"{'Begin date:':<15} {tournament.get('date_begin', '')}")
        print(f"{'End date:':<15} {tournament.get('date_end', '')}")
        print(f"{'Round actual:':<15} {tournament.get('round_actual', '')}")
        print(f"{'Rounds max:':<15} {tournament.get('rounds_max', '')}")
        print(f"{'Status:':<15} {tournament.get('status', '')}\n\n")

    def display_tournament_players(players):
        """
        Displays the list of players participating in the tournament.

        Args:
        - players: A list of dictionaries containing the details of the players.
        """

        print_section("| Players |", SECTION_CHAR, SECTION_WIDTH)
        print()
        print(f"{'FIRST NAME':<30} {'LAST NAME':<30}")
        print_section("", SECTION_CHAR, SECTION_WIDTH)
        for i, player in enumerate(players, 1):
            print(
                f"{player.get('first_name', ''):<30} "
                f"{player.get('last_name', ''):<30} "
            )
        print("\n")

    def display_ranking(players_score):
        """
        Displays the ranking and scoring of players in the tournament.

        Args:
        - players_score: A list of dictionaries containing the details of the players and their scores.
        """

        print_section("| Players ranking |", SECTION_CHAR, SECTION_WIDTH)
        print()
        print(f"{'RANK':<5} {'FIRST NAME':<30} {'LAST NAME':<30} {'SCORE':<8}")
        print_section("", SECTION_CHAR, SECTION_WIDTH)
        for i, player in enumerate(players_score, 1):
            print(
                f"{str(i):<6} "
                f"{player.get('first_name', ''):<30} "
                f"{player.get('last_name', ''):<30} "
                f"{player.get('score', '')} "
            )
        print("\n")

    def display_round(round):
        """
        Displays the details of a round.

        Args:
        - round: A dictionary containing the details of the round.
        """

        print_section("| Round Details |", SECTION_CHAR, SECTION_WIDTH)
        print(f"\n{'Name':<15} {round.get('round_name', '')}")
        print(f"{'Start date:':<15} {round.get('datetime_begin', '')}")
        print(f"{'End date:':<15} {round.get('datetime_end', '')}")
        print(f"{'Status:':<15} {round.get('status', '')}\n\n")

    def display_matches(matches_list):
        """
        Displays the matches of the tournament, the players and the scores.

        Args:
        - matches_list: A list of dictionaries containing the details of the matches.
        """

        print(f"{'#':<5} {'Player (WHITES)':<29} {'Player (BLACKS)':<30} {'SCORE':<6} ")
        print_section("", SECTION_CHAR, SECTION_WIDTH)
        for i, match in enumerate(matches_list, 1):
            print(
                f"#{str(i):<5}"
                f"{match.get('first_name_A', '') + ' ' + match.get('last_name_A', ''):<30}"
                f"{match.get('first_name_B', '') + ' ' + match.get('last_name_B', ''):<30}"
                f"({match.get('score_A', ''):<3} , "
                f"{match.get('score_B', ''):<3})"
            )
        print("\n")

    def display_message(message=""):
        """
        Displays a message or "Press key to continue..."

        Args:
        - message (optional): A string representing the message to be displayed.
        """

        if message:
            input(f"\n{message}, press key to continue...")
        else:
            input("\nPress key to continue...")

    def clear_screen():
        """Clears the screen."""

        clear_screen()
