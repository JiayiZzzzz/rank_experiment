from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'self_esteem_scale'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4], widget=widgets.RadioSelect)


class Player(BasePlayer):
    q1 = make_q('1. 整体而言，我对自己感到满意')
    q2 = make_q('2. 有时我觉得自己一点都不好')
    q3 = make_q('3. 我觉得我有许多优点')
    q4 = make_q('4. 我做事可以做得和大多数人一样好')
    q5 = make_q('5. 我觉得自己没有什么值得自豪的地方')
    q6 = make_q('6. 有时我确实觉得自己一无是处')
    q7 = make_q('7. 我认为自己是个有价值的人，至少与别人不相上下')
    q8 = make_q('8. 我希望我能多尊重自己一些')
    q9 = make_q('9. 总的来说，我倾向于认为自己是一个失败者')
    q10 = make_q('10. 我对自己持有一种正面态度')

    self_esteem = models.FloatField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.self_esteem = player.q1 + player.q3 + player.q4 + player.q7 + player.q10 \
                            - (player.q2 + player.q5 + player.q6 + player.q8 + player.q9)


page_sequence = [MyPage]
