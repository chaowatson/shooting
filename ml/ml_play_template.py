import random


class MLPlay:
    def __init__(self):
        print("Initial ml script")
        self.counter = 0

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        else:
            return ["UP"]



    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
