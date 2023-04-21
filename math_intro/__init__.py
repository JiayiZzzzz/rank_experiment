from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'math_intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class PracticeIntro1(Page):
    pass


class PracticeIntro2(Page):
    pass


page_sequence = [PracticeIntro1, PracticeIntro2]
