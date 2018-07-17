import random
import pandas as pd

TRIALS = 1000

def count_successes(seq):
    return seq.count(8) + seq.count(9) + seq.count(10)

class System:
    def __init__(self, pool):
        self.pool = pool

    def roll(self):
        raise NotImplementedError

    @classmethod
    def test(cls, min=1, max=20, trials=TRIALS):
        df = pd.DataFrame()
        for pool in range(min, max):
            system_instance = cls(pool)

            rolls = dict()
            for i in range(trials):
                result = system_instance.roll()
                rolls[result] = rolls.get(result, 0) + 1
            df[pool] = pd.Series(rolls)
        return df / trials

class DiceSystem(System):
    def __init__(self, pool, sides=10, difficulty=8):
        super().__init__(pool)
        self.sides = 10
        self.difficulty = 8

    def roll(self, again=10):
        dice_results = []
        counter = 0
        while counter < self.pool:
            next_roll = random.randint(1, self.sides)
            if next_roll < again:
                counter += 1
            dice_results.append(next_roll)

        return count_successes(dice_results)

class DefaultDiceSystem(DiceSystem):
    def __init__(self, pool):
        super().__init__(pool, sides=10, difficulty=8)

class CardSystem(System):
    def __init__(self, pool, first_threshold, threshold_increment, cards):
        super().__init__(pool)
        self.first_threshold = first_threshold
        self.threshold_increment = threshold_increment
        self.cards = cards

    def roll(self, again=10):
        this_roll = random.choice(self.cards)
        total = self.pool + this_roll
        if this_roll >= again:
            total += self.roll()

        irrelevant_part = self.first_threshold - self.threshold_increment
        relevant_part = total - irrelevant_part
        successes = relevant_part // self.threshold_increment
        return max(successes, 0)

class OldEightThreeCardSystem(CardSystem):
    def __init__(self, pool):
        super().__init__(pool, first_threshold=8, threshold_increment=3, cards=[-1000, 2, 3, 4, 5, 6, 7, 8, 9, 10])

class JokersEightThreeCardSystem(CardSystem):
    def __init__(self, pool):
        super().__init__(pool, first_threshold=8, threshold_increment=3, cards=[-5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

class JokersTenThreeCardSystem(CardSystem):
    def __init__(self, pool):
        super().__init__(pool, first_threshold=10, threshold_increment=3, cards=[-5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


if __name__ == '__main__':
    dds_df = DefaultDiceSystem.test()
    oetcs_df = OldEightThreeCardSystem.test()
    jetcs_df = JokersEightThreeCardSystem.test()
    jttcs_df = JokersTenThreeCardSystem.test()

    print(dds_df)
