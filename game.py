"""
This module defines the Game class, which is the simulation.
"""

import random

class Game:
    """
    A singular isolated community of only hawks and doves with
    varying initial parameters. This is also referred to a single
    "simulation" or "game."
    """

    def __init__(self, birds, p_doves, carrying_cap, r):
        """
        Game of hawks and doves
        """

        self.doves = int((birds * p_doves)//1)
        self.hawks = birds - self.doves
        self.carrying_cap = carrying_cap
        self.r = r
        self.chosen_doves = 0
        self.chosen_hawks = 0

        self.game_matrix = [
            [(0, None), (1, 0.25)],
            [(1, 0.25), (None, 11/12)]
        ]

    def choose_pair(self):
        """
        Chooses up to 2 random birds and return them

        returns [Optional 0|1, Optional 0|1]
        """

        # Calculate true number of hawks and doves
        doves = self.doves - self.chosen_doves
        hawks = self.hawks - self.chosen_hawks

        # Return list with single element if only 1 available, empty list if none
        if doves + hawks < 2:
            if doves == 1:
                return [1]
            elif hawks == 1:
                return [0]
            else:
                return []

        # Chose 2 random birds
        chosen = []
        for _ in range(2):
            doves = self.doves - self.chosen_doves
            hawks = self.hawks - self.chosen_hawks
            if random.random() < doves/(doves + hawks):
                chosen.append(1)
                self.chosen_doves += 1
            else:
                chosen.append(0)
                self.chosen_hawks += 1

        # Return result
        return chosen

    def generate_pairs(self):
        """
        Randomly pairs entire bird population and returns pairs

        returns list([Optional 0|1, Optional 0|1])
        """

        # Reset chosen counts
        self.chosen_doves = 0
        self.chosen_hawks = 0

        # Generate all pairs
        pairs = []
        for _ in range(int((self.carrying_cap+1)//2)):
            pairs.append(self.choose_pair())

        # Return result
        return pairs

    def evaluate_pair(self, pair):
        """
        Evaluates the given pair and determines the number of surviving hawks and doves

        pair [Optional 0|1, Optional 0|1]: the pair of birds

        returns [surviving hawks 0|1|2, suriving doves 0|1|2]
        """

        # Edge cases of empty and single-element pairs
        if len(pair) == 0:
            return [0, 0]
        elif len(pair) == 1:
            survived = [0, 0]
            survived[pair[0]] = 1
            return survived

        # Generate survival probabilities
        matrix_cell = self.game_matrix[pair[0]][pair[1]]
        hawk_survival_prob = matrix_cell[0]
        dove_survival_prob = matrix_cell[1]

        # Randomly die
        survived = [0, 0]

        for i in pair:
            if i == 0:
                if random.random() < hawk_survival_prob:
                    survived[0] += 1
            elif i == 1:
                if random.random() < dove_survival_prob:
                    survived[1] += 1

        # Return result
        return survived

    def kill_birds(self):
        """
        Pairs birds and kills birds that randomly died
        """

        # Generate all pairs
        pairs = self.generate_pairs()

        # Count surviving birds
        survived = [0, 0]

        for pair in pairs:
            live_hawks, live_doves = self.evaluate_pair(pair)
            survived = [survived[0] + live_hawks, survived[1] + live_doves]

        # Update counts
        self.hawks = survived[0]
        self.doves = survived[1]

    def exponential_growth(self):
        """
        Allows all birds to increase in population exponentially
        """

        self.doves += self.r*self.doves
        self.hawks += self.r*self.hawks

    def day(self):
        """
        Updates the number of birds after 1 day
        """

        self.exponential_growth()
        self.kill_birds()
