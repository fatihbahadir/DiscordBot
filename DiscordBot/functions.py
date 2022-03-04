from random import randint

class Game:

    @staticmethod
    def roll_dice():
        return randint(1, 7)

    @staticmethod
    def flip_coin():
        coin = ["head", "tail"]
        selected = coin[randint(0,2)]
        return selected