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
        # e = random.randint(10, 99)
        # result = a + b + c + d + e
        # string = '%2d + %2d + %2d + %2d + %2d= ? ' % (a, b, c, d, e)
        result = a * b * c * d
        string = '%2d x %2d x %2d x %2d = ? ' % (a, b, c, d)
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
    NAME_IN_URL = 'ranking_round'
    PLAYERS_PER_GROUP = 6
    TIMER_TEXT = "Time to complete this section:"
    time_limit = 300
    ROUNDS_PER_SG = [40]
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
    rank_info = models.StringField()
    answer = models.IntegerField(label='请输入您的答案：', min=1000, max=100000000, blank=True)
    is_correct = models.BooleanField()
    is_quit = models.BooleanField(initial=False)
    is_eliminated = models.BooleanField(initial=False)
    start_eliminate = models.BooleanField(initial=False)
    eliminate_count = models.IntegerField(initial=1)


def live_method(player, data):
    players = player.group.get_players()
    players.sort(key=lambda p: p.participant.forced_total_correct, reverse=True)
    if 'quit' in data:
        player.is_quit = data['quit']
    if 'eliminate' in data:
        player.start_eliminate = data['eliminate']
        if player.eliminate_count == 1:
            players[5].is_eliminated = True
            player.eliminate_count += 1
            if players[5].participant.forced_status == 'STAY':
                players[5].participant.forced_status = 'ELIMINATED'
                players[5].participant.forced_duration = 120
                return {players[5].id_in_group: 1}
        elif player.eliminate_count == 2:
            players[4].is_eliminated = True
            player.eliminate_count += 1
            if players[4].participant.forced_status == 'STAY':
                players[4].participant.forced_status = 'ELIMINATED'
                players[4].participant.forced_duration = 180
                return {players[4].id_in_group: 1}
        elif player.eliminate_count == 3:
            players[3].is_eliminated = True
            player.eliminate_count += 1
            if players[3].participant.forced_status == 'STAY':
                players[3].participant.forced_status = 'ELIMINATED'
                players[3].participant.forced_duration = 240
                return {players[3].id_in_group: 1}
        # return {players[-1].id_in_group: 1}


def get_timeout_seconds1(player: Player):
    participant = player.participant
    group = player.group
    players = group.get_players()
    players.sort(key=lambda p: p.participant.forced_total_correct, reverse=True)

    import time
    return participant.expiry - time.time()


def player_rank_sort(group):
    players = group.get_players()
    players.sort(key=lambda p: p.participant.forced_total_correct, reverse=True)
    for i in range(len(players)):
        if i > 0 and players[i].participant.forced_total_correct == players[i - 1].participant.forced_total_correct:
            rank = players[i - 1].rank
        else:
            rank = i + 1
        players[i].rank = rank
        players[i].participant.forced_rank = rank
        if players[i].rank < 0.5 * len(players):
            players[i].rank_info = "前1/2"
        else:
            players[i].rank_info = "后1/2"


# PAGES
class FRIntro(Page):

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        participant = player.participant
        import time
        if subsession.round_number == 1:
            participant.forced_total_correct = 0
            participant.forced_total_attempt = 0
            participant.forced_duration = C.time_limit
            participant.forced_status = 'STAY'
            participant.expiry = time.time() + C.time_limit
            participant.forced_track_1min_correct = 0
            participant.forced_track_2min_correct = 0
            participant.forced_track_3min_correct = 0
            participant.forced_track_4min_correct = 0
            participant.forced_track_1min_attempt = 0
            participant.forced_track_2min_attempt = 0
            participant.forced_track_3min_attempt = 0
            participant.forced_track_4min_attempt = 0
            participant.forced_rank = 0

        return subsession.period == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group
        # print('所有玩家：', group.get_players())
        # print('play前最后一位玩家：', group.get_players()[-1])
        return dict(num_players=len(group.get_players()))


class ResultsWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        player_rank_sort(group)

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
        participant = player.participant
        players = player.group.get_players()
        players.sort(key=lambda p: p.participant.forced_total_correct, reverse=True)
        # out_id = players[-1].id_in_group
        if participant.forced_status == 'QUIT' or participant.forced_status == 'ELIMINATED':
            return False
        elif player.is_eliminated:
            return False
        else:
            player_rank_sort(player.group)
            if get_timeout_seconds1(player) <= C.time_limit - 60 and participant.forced_track_1min_correct == 0:
                participant.forced_track_1min_correct = participant.forced_total_correct
                participant.forced_track_1min_attempt = participant.forced_total_attempt

            if get_timeout_seconds1(player) <= C.time_limit - 120 and participant.forced_track_2min_correct == 0:
                participant.forced_track_2min_correct = participant.forced_total_correct
                participant.forced_track_2min_attempt = participant.forced_total_attempt

            if get_timeout_seconds1(player) <= C.time_limit - 180 and participant.forced_track_3min_correct == 0:
                participant.forced_track_3min_correct = participant.forced_total_correct
                participant.forced_track_3min_attempt = participant.forced_total_attempt

            if get_timeout_seconds1(player) <= C.time_limit - 240 and participant.forced_track_4min_correct == 0:
                participant.forced_track_4min_correct = participant.forced_total_correct
                participant.forced_track_4min_attempt = participant.forced_total_attempt
            return get_timeout_seconds1(player) > 0

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        player.question = C.ques[player.round_number - 1]
        print('ques in round ', player.round_number, ' is: ', player.question, 'ans is: ',
              C.ans[player.round_number - 1])
        return dict(num_players=len(group.get_players()))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        # print('ans: ', player.field_maybe_none('answer'), ' cor ans: ', C.ans[player.round_number - 1])
        if player.field_maybe_none('answer') == C.ans[player.round_number - 1] and player.is_quit == 0:
            player.is_correct = True
            participant.forced_total_correct += 1
            participant.forced_total_attempt += 1
            return True
        elif player.field_maybe_none('answer') != C.ans[player.round_number - 1] and player.is_quit == 0:
            player.is_correct = False
            participant.forced_total_attempt += 1
            return True
        elif player.is_quit:
            if participant.forced_status == 'STAY':
                participant.forced_status = 'QUIT'
            if participant.forced_duration == C.time_limit:
                participant.forced_duration = C.time_limit - get_timeout_seconds1(player)
                # print('quit time:', participant.forced_duration)
            return False


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS or player.is_quit or player.is_eliminated

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_players=player.in_all_rounds())


page_sequence = [FRIntro, ResultsWaitPage, MathGame, Results]
