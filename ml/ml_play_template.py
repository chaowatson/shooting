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
            self.counter += 1
            if self.counter < 7:
                return ["LEFT_TURN"]
            elif self.counter >= 7 and self.counter < 29:
                return ["UP", "SHOOT"]
            elif self.counter < 35:
                return ["RIGHT_TURN"]
            elif self.counter >= 35 and self.counter < 60:
                return ["UP", "SHOOT"]
            elif self.counter < 66:
                return ["LEFT_TURN"]
            elif self.counter >= 66 and self.counter < 99:
                return ["UP", "SHOOT"]
            elif self.counter < 105:
                return ["LEFT_TURN"]
            elif self.counter >= 105 and self.counter < 127:
                return ["UP", "SHOOT"]
            elif self.counter < 133:
                return ["RIGHT_TURN"]
            elif self.counter >= 133 and self.counter < 180:
                return ["UP", "SHOOT"]
            elif self.counter < 186:
                return ["RIGHT_TURN"]
            elif self.counter >= 186 and self.counter < 230:
                return ["UP", "SHOOT"]
            elif self.counter < 236:
                return ["RIGHT_TURN"]
            elif self.counter >= 236 and self.counter < 275:
                return ["UP", "SHOOT"]
            elif self.counter < 281:
                return ["LEFT_TURN"]
            elif self.counter >= 281 and self.counter < 310:
                return ["UP", "SHOOT"]
            else:
                return ["UP", "RIGHT_TURN"]


    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
