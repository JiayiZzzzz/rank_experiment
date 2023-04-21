from otree.api import *
import random

doc = """
Piece-rate
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
    NAME_IN_URL = 'piece_rate'
    PLAYERS_PER_GROUP = 6
    TIMER_TEXT = "Time to complete this section:"
    time_limit = 300
    ROUNDS_PER_SG = [180]  #一共多少道题，这里需要改
    SG_ENDS = cumsum(ROUNDS_PER_SG)
    NUM_ROUNDS = sum(ROUNDS_PER_SG)
    # print('num round: ', NUM_ROUNDS)
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
        # print('有', len(subsession.get_players()), '个玩家')
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
    rank = models.IntegerField()
    answer = models.IntegerField(label='请输入您的答案：', min=50, max=500, blank=True)
    is_correct = models.BooleanField()
    is_quit = models.BooleanField(initial=False)


def live_method(player, data):
    if 'quit' in data:
        player.is_quit = data['quit']
        # print('live method quit is: ', player.is_quit)


def get_timeout_seconds1(player: Player):
    participant = player.participant
    import time

    return participant.expiry - time.time()


# PAGES
class PRIntro(Page):

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        participant = player.participant
        import time
        if subsession.round_number == 1:
            participant.piece_total_correct = 0
            participant.piece_total_attempt = 0
            participant.piece_duration = C.time_limit
            participant.piece_status = 'STAY'
            participant.expiry = time.time() + C.time_limit
            participant.piece_track_1min_correct = 0
            participant.piece_track_2min_correct = 0
            participant.piece_track_3min_correct = 0
            participant.piece_track_4min_correct = 0
            participant.piece_rank = 0

        return subsession.period == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        return dict(num_players=len(group.get_players()))


class MyWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        players.sort(key=lambda p: p.participant.piece_total_correct)
        for i in range(len(players)):
            if i > 0 and players[i].participant.piece_total_correct == players[i - 1].participant.piece_total_correct:
                rank = players[i - 1].rank
            else:
                rank = i + 1
            players[i].rank = rank
            players[i].participant.piece_rank = rank

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1


class MathGame(Page):
    live_method = live_method
    get_timeout_seconds = get_timeout_seconds1
    timer_text = C.TIMER_TEXT
    form_model = "player"
    form_fields = ['answer']

    @staticmethod
    def is_displayed(player: Player):
        # subsession = player.subsession
        participant = player.participant
        if participant.piece_status == 'QUIT':
            # print('您已选择退出游戏')
            return False
        else:
            group = player.group
            players = group.get_players()
            players.sort(key=lambda p: p.participant.piece_total_correct, reverse=True)
            for i in range(len(players)):
                if i > 0 and players[i].participant.piece_total_correct \
                        == players[i - 1].participant.piece_total_correct:
                    rank = players[i - 1].rank
                else:
                    rank = i + 1
                players[i].rank = rank
                players[i].participant.piece_rank = rank

            participant = player.participant
            # 这里应该只能记录四个，得时刻记得改
            if get_timeout_seconds1(player) <= C.time_limit - 60 and participant.piece_track_1min_correct == 0:
                participant.piece_track_1min_correct = participant.piece_total_correct
            if get_timeout_seconds1(player) <= C.time_limit - 120 and participant.piece_track_2min_correct == 0:
                participant.piece_track_2min_correct = participant.piece_total_correct

            if get_timeout_seconds1(player) <= C.time_limit - 180 and participant.piece_track_3min_correct == 0:
                participant.piece_track_3min_correct = participant.piece_total_correct
            if get_timeout_seconds1(player) <= C.time_limit - 240 and participant.piece_track_4min_correct == 0:
                participant.piece_track_4min_correct = participant.piece_total_correct   

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
        # print('ans: ', player.field_maybe_none('answer'), ' cor ans: ', C.ans[player.round_number - 1])
        if player.field_maybe_none('answer') == C.ans[player.round_number - 1] and player.is_quit == 0:
            player.is_correct = True
            participant.piece_total_correct += 1
            participant.piece_total_attempt += 1
            return True
        elif player.field_maybe_none('answer') != C.ans[player.round_number - 1] and player.is_quit == 0:
            player.is_correct = False
            participant.piece_total_attempt += 1
            # print('attempt times: ', participant.piece_total_attempt)
            # print('correct times: ', participant.piece_total_correct)
            return True
        elif player.is_quit:
            if participant.piece_status == 'STAY':
                participant.piece_status = 'QUIT'
            if participant.piece_duration == C.time_limit:
                participant.piece_duration = C.time_limit - get_timeout_seconds1(player)
                # print('quit time:', participant.piece_duration)
            return False


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS or player.is_quit

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_players=player.in_all_rounds())


page_sequence = [PRIntro, MyWaitPage, MathGame, Results]
