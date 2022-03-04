import random


class MLPlay:
    def __init__(self):
        print("Initial ml script")
        self.counter = 0

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """

        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        else:
            pass



    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
