import random
import datetime


class Memoize(type):
    _instance = {}
    memoization_limit: int = 10
    memoization: list[float] = []
    weighted_limits: dict[str, float] = {
        "Rock": 1.0,
        "Paper": 2.0,
        "Scissors": 3.0
    }

    def __call__(cls):
        if cls not in cls._instance:
            cls._instance[cls] = super(Memoize, cls).__call__()
        return cls._instance[cls]

    def memoize(self) -> int:
        random.seed(datetime.datetime.now())
