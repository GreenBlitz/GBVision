from exceptions import AbstractMethodCallingException
from utils import GameObject


class ObjectFinder:
    def __init__(self, threshold_func, game_object: GameObject):
        self.threshold = threshold_func
        self.game_object = game_object

    def __call__(self, frame, camera):
        raise AbstractMethodCallingException()
