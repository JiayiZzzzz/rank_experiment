from otree.api import *
from random import randint

doc = """
brief assessment questionnaire
"""


def rank_scale(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5, 6], widget=widgets.RadioSelectHorizontal)


def psych_scale(label):
    return models.IntegerField(label=label, choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                               widget=widgets.RadioSelectHorizontal)


class C(BaseConstants):
    NAME_IN_URL = 'brief_assessment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.participant.rank_guess = 0
        p.participant.math_task_pay = ''


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = rank_scale('1.	请估计您在piece-rate round中的小组排名：')

    q2 = psych_scale('2. 请评估一下您在task session中的压力程度'
                     '(0 表示毫无压力, 10 表示压力非常大)')
    q3 = psych_scale('3. 请评估一下您在task session中的高兴程度'
                     '(0 表示毫不高兴, 10 表示非常高兴)')
    q4 = psych_scale('4. 请评估一下您在task session中的紧张程度'
                     '(0 表示毫不紧张, 10 表示非常紧张)')
    q5 = psych_scale('5. 请评估一下您在task session中的生气程度'
                     '(0 表示毫不生气, 10 表示非常生气)')
    q6 = psych_scale('6. 请评估一下您在task session中的兴奋程度'
                     '(0 表示毫不兴奋, 10 表示非常兴奋)')


# PAGES
class Rank(Page):
    form_model = 'player'
    form_fields = ['q1']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.rank_guess = player.q1
        if participant.rank_guess == participant.piece_rank:
            participant.payoff += 0.5


class Psych1(Page):
    form_model = 'player'
    form_fields = ['q2', 'q3', 'q4', 'q5', 'q6']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        draw = randint(0, 1)
        participant = player.participant
        if draw == 1:
            participant.math_task_pay = 'Piece rate round'
            participant.payoff += 0.25 * participant.piece_total_correct
        else:
            participant.math_task_pay = 'Forced ranking round'
            participant.payoff += 0.25 * participant.forced_total_correct
            if participant.forced_rank == 1:
                participant.payoff += 5  #这里需要改


class Results(Page):
    form_model = "player"


page_sequence = [Rank, Psych1, Results]
