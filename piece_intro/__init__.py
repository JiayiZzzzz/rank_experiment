from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'piece_intro'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class PRIntro(Page):
    form_model = 'player'


page_sequence = [PRIntro]
