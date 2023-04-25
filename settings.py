from os import environ


"""
app_sequence=['introduction', 'consent', 'demographic_question', 'math_intro', 'practice_round', 
'piece_rate', 'ranking_round', 
'estimation_emotion', 'self_esteem_scale', 'big_five', 'PEI', 'gamble_choice'],
"""
SESSION_CONFIGS = [
    dict(
        name='Spade',
        app_sequence=['introduction', 'demographic_question', 'math_intro', 'practice_round',
                      'piece_rate', 'ranking_round',
                      'estimation_emotion', 'self_esteem_scale', 'big_five', 'PEI', 'gamble_choice'],
        num_demo_participants=6,
    ),
    dict(
        name='Heart',
        app_sequence=['introduction', 'demographic_question', 'math_intro', 'practice_round',
                      'ranking_round', 'piece_rate',
                      'estimation_emotion', 'self_esteem_scale', 'big_five', 'PEI', 'gamble_choice'],
        num_demo_participants=6,
    ),
    dict(
        name='Diamond',
        app_sequence=['introduction', 'demographic_question', 'math_intro', 'practice_round',
                      'piece_rate', 'ranking_round',
                      'estimation_emotion', 'self_esteem_scale', 'big_five', 'PEI', 'gamble_choice'],
        num_demo_participants=6,
    ),
]
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'expiry',
    'practice_correct',
    'piece_total_correct',
    'piece_total_attempt',
    'piece_duration',
    'piece_status',
    'piece_rank',
    'piece_track_1min_correct',
    'piece_track_2min_correct',
    'piece_track_3min_correct',
    'piece_track_4min_correct',
    'piece_track_1min_attempt',
    'piece_track_2min_attempt',
    'piece_track_3min_attempt',
    'piece_track_4min_attempt',
    'forced_total_correct',
    'forced_total_attempt',
    'forced_duration',
    'forced_status',
    'forced_rank',
    'forced_track_1min_correct',
    'forced_track_2min_correct',
    'forced_track_3min_correct',
    'forced_track_4min_correct',
    'forced_track_1min_attempt',
    'forced_track_2min_attempt',
    'forced_track_3min_attempt',
    'forced_track_4min_attempt',
    'math_task_pay',
    'rank_guess',
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'zh-hans'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8592383501810'
