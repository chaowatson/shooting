import random


class MLPlay:
    def __init__(self):
        print("Initial ml script")
        self.counter = 0

    def update(self, scene_info: dict, *args,**kwargs):
        """
        Generate the command according to the received scene information
        """
        print("enemies at : ", scene_info["enemies_position"][0], "player at : ", scene_info["player_position"]
              , "player angle : ", scene_info["player_angle"], "aids at : ", scene_info["aids_position"][0], "goals at : ",
              scene_info["goals"])

        actions=[
            "UP",
            "DOWN",
            "LEFT_TURN",
            "RIGHT_TURN",
            "SHOOT"
        ]
        # print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        else:
            return random.sample(actions,1)



    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
