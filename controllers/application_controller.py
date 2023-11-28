from controllers.menu_controller import ControllerMenuHome


class ControllerApplication:
    """This class is responsible for starting the application and
    managing the flow of control between different menu controllers."""

    def __init__(self):
        self.controller = None

    def start(self):
        """Main loop for the menu controller"""
        self.controller = ControllerMenuHome()
        while self.controller:
            self.controller = self.controller()
