from otree.api import*
from typing import Dict
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c)
from random import randint

doc = """
Your app description
"""

'''
    list_high = [C.choice_1_high, C.choice_2_high, C.choice_3_high, C.choice_4_high,
                 C.choice_5_high, ]
    list_low = [C.choice_1_low, C.choice_2_low, C.choice_3_low, C.choice_4_low,
                C.choice_5_low, ]
'''


class C(BaseConstants):
    NAME_IN_URL = 'Lottery_test'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # Payoffs depending on the situation

    payoff_matrix: Dict[str, Dict[int, c]] = {
        '正面':
            {
                1: c(4),
                2: c(6),
                3: c(8),
                4: c(10),
                5: c(12)
            },
        '反面':
            {
                1: c(4),
                2: c(3),
                3: c(2),
                4: c(1),
                5: c(0)
            }
    }

    choice_1_low = 4
    choice_2_low = 3
    choice_3_low = 2
    choice_4_low = 1
    choice_5_low = 0

    choice_1_high = 4
    choice_2_high = 6
    choice_3_high = 8
    choice_4_high = 10
    choice_5_high = 12


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery_choice = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
    )

    gain = models.CurrencyField(initial=c(0))
    event = models.StringField()

    def set_gain(self, r):
        self.event = r
        self.gain = C.payoff_matrix[self.event][self.lottery_choice]
        self.payoff += self.gain


# PAGES


class TheLotteryTaskCN(Page):
    form_model = "player"
    form_fields = ['lottery_choice']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        event = randint(0, 1)
        if event == 1:
            player.set_gain('正面')
        else:
            player.set_gain('反面')


class ResultsCN(Page):
    form_model = "player"


page_sequence = [TheLotteryTaskCN, ResultsCN]
