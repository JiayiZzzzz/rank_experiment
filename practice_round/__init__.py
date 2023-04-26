from otree.api import *
import random

doc = """
Your app description
"""


def problem_set(num, ques, ans):
    for i in range(0, num):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        c = random.randint(10, 99)
        d = random.randint(10, 99)
        e = random.randint(10, 99)
        result = a + b + c + d + e
        string = '%2d + %2d + %2d + %2d + %2d= ? ' % (a, b, c, d, e)
        ques.append(string)
        ans.append(result)
    return ques, ans


def cumsum(lst):
    total = 0
    new = []
    for ele in lst:
        total += ele
        new.append(total)
    return new


class C(BaseConstants):
    NAME_IN_URL = 'practice_round'
    PLAYERS_PER_GROUP = None
    TIMER_TEXT = "Time to complete this section:"
    ROUNDS_PER_SG = [30]
    SG_ENDS = cumsum(ROUNDS_PER_SG)
    NUM_ROUNDS = sum(ROUNDS_PER_SG)
    problem_num = NUM_ROUNDS
    ques = []
    ans = []
    ques, ans = problem_set(problem_num, ques, ans)


class Subsession(BaseSubsession):
    sg = models.IntegerField()
    period = models.IntegerField()
    is_last_period = models.BooleanField()


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        sg = 1
        period = 1
        for ss in subsession.in_rounds(1, C.NUM_ROUNDS):
            ss.sg = sg
            ss.period = period
            is_last_period = ss.round_number in C.SG_ENDS
            ss.is_last_period = is_last_period
            if is_last_period:
                sg += 1
                period = 1
            else:
                period += 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question = models.StringField()
    answer = models.IntegerField(label='请输入您的答案：', min=50, max=500, blank=True)
    is_correct = models.BooleanField()


def get_timeout_seconds1(player: Player):
    participant = player.participant
    import time
    return participant.expiry - time.time()


"""
def is_displayed1(player: Player):
    return get_timeout_seconds1(player) > 0
"""


# PAGES
class Intro(Page):

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        participant = player.participant
        import time
        if subsession.round_number == 1:
            participant.practice_correct = 0
            participant.expiry = time.time() + 60
        return subsession.period == 1


class MathGame(Page):
    get_timeout_seconds = get_timeout_seconds1
    timer_text = C.TIMER_TEXT
    form_model = "player"
    form_fields = ['answer']

    @staticmethod
    def is_displayed(player: Player):
        return get_timeout_seconds1(player) > 0

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        player.question = C.ques[player.round_number - 1]
        print('ques in round ', C.ques[player.round_number - 1], ' is: ', player.question, 'ans is: ',
              C.ans[player.round_number - 1])
        return dict(num_players=len(group.get_players()))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        print('ans: ', player.field_maybe_none('answer'), ' cor ans: ', C.ans[player.round_number - 1])
        if player.field_maybe_none('answer') == C.ans[player.round_number - 1]:
            player.is_correct = True
            participant.practice_correct += 1
        else:
            player.is_correct = False
        return True


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_players=player.in_all_rounds())


page_sequence = [Intro, MathGame, Results]
