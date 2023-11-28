from utils.utils import clear_screen

SECTION_WIDTH = 80


class ViewGame:
    """
    This class provides methods for selecting:
        a match
        updating the score of a match
        displaying messages
        clearing the screen
    """

    def select_match(matches_list):
        """Selects a match from a list of matches."""
        if not matches_list:
            print("The matches list is currently empty.")
            return None
        num_of_matches = len(matches_list)
        prompt_str = (
            f"Enter the line number of the match to select (1-{num_of_matches}): "
        )
        while True:
            try:
                line_number = int(input(prompt_str))
                if line_number < 1 or line_number > num_of_matches:
                    raise ValueError()
                match_selected = matches_list[line_number - 1]
                return match_selected
            except ValueError:
                print(
                    f"Invalid input format. Please enter an integer between 1 and {num_of_matches}."
                )

    def update_score_match(match_selected):
        """Updates the score of a selected match."""
        while True:
            user_answer = input(
                'Enter the result for the Whites: (1) Win, (2) Lose, (3) Draw or press "Enter" to cancel: '
            )
            if user_answer in ("1", "2", "3", ""):
                if user_answer == "1":
                    match_selected["score_A"] = "1"
                    match_selected["score_B"] = "0"
                if user_answer == "2":
                    match_selected["score_A"] = "0"
                    match_selected["score_B"] = "1"
                if user_answer == "3":
                    match_selected["score_A"] = "0.5"
                    match_selected["score_B"] = "0.5"
                break
            print("Please enter a valid option.")
        return match_selected

    def display_message(message=""):
        """Displays a message to the user."""
        if message:
            input(f'\n{message}, press "Enter" to continue...')
        else:
            input('\nPress "Enter" to continue...')

    def clear_screen():
        """Clears the screen."""
        clear_screen()
