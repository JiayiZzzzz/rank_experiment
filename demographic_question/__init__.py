from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'demographic_question'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='1. 请输入您的年龄', min=15, max=120)
    gender = models.StringField(
        choices=[['男性', '男性'], ['女性', '女性']],
        label='2. 请输入您的性别',
        widget=widgets.RadioSelect,
    )
    school = models.StringField(
        choices=['文学类', '历史学类', '哲学类',
                 '法学类', '经济学类', '管理学类', '教育学类', '理学类', '工学类',
                 '农学类', '医学类', '军事学类',
                 '艺术学类', '其它'],
        label='3. 请输入您的学科专业',
        widget=widgets.RadioSelect,
    )
    degree = models.StringField(
        choices=['高中生及以下', '本科生', '研究生', '博士生',
                 '博士后'],
        label='4. 请选择您的受教育程度',
        widget=widgets.RadioSelect,
    )
    """
    other = models.LongStringField(
        label='If you select other, please type in your major here  '
    )
    choices=['Computer Science', 'Economics and Management', 'Engineering',
                 'Humanities', 'Law', 'Life Sciences', 'Mathematics', ' Natural Science', 'Psychology'
                 'Social Sciences and Education', 'Teaching and Education', 'Other'],
    """


# PAGES
class Demographic(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'school', 'degree']


page_sequence = [Demographic]
