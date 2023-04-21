from otree.api import *


doc = """
Big 5 personality test
"""


class C(BaseConstants):
    NAME_IN_URL = 'big_five'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelect)


# BFI-10 Taiwanese Items
class Player(BasePlayer):
    q1 = make_q('比较放不开')
    q2 = make_q('容易相信别人')
    q3 = make_q('比较懒')
    q4 = make_q('懂得放松而且会处理压力')
    q5 = make_q('艺术方面的兴趣较少')
    q6 = make_q('外向，善于社交')
    q7 = make_q('比较会挑人毛病')
    q8 = make_q('工作有始有终')
    q9 = make_q('容易紧张')
    q10 = make_q('想象力丰富')

    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    conscientiousness = models.FloatField()
    neuroticism = models.FloatField()
    openness = models.FloatField()


def combine_score(positive, negative):
    return 3 + (positive - negative) / 2


# PAGES
class BigFive(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.extraversion = combine_score(player.q6, player.q1)
        player.agreeableness = combine_score(player.q2, player.q7)
        player.conscientiousness = combine_score(player.q8, player.q3)
        player.neuroticism = combine_score(player.q9, player.q4)
        player.openness = combine_score(player.q10, player.q5)


page_sequence = [BigFive]
