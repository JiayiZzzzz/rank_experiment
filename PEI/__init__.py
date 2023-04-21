from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'PEI'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4], widget=widgets.RadioSelect)


class Player(BasePlayer):
    q1 = make_q('1. 我是个会交际的人')
    q2 = make_q('2. 近几天来有好几次我对自己非常失望')
    q3 = make_q('3. 使我烦恼的是我的模样不能更好看点')
    q4 = make_q('4. 维持一个令人满意的爱情关系对我没有困难')
    q5 = make_q('5. 我此刻比过去几周更为快乐')
    q6 = make_q('6. 我对我的身体外貌很满意')
    q7 = make_q('7. 有时我不去参加球类及非正式的体育活动，因此我认为自己对此不擅长')
    q8 = make_q('8. 当众讲话会使我不舒服')
    q9 = make_q('9. 我希望认识更多的人，可我又不愿外出和同他们见面')
    q10 = make_q('10. 体育运动是我的擅长领域之一')

    q11 = make_q('11. 学习成绩是一个我可以展示自己能力，并因自己的成就而获得认可的领域')
    q12 = make_q('12. 我长得比一般人好看')
    q13 = make_q('13. 在公共场合表演节目和讲话，我想都不敢想')
    q14 = make_q('14. 想到大多数体育活动时，我便充满热情和渴望，而不是疑惧和焦虑')
    q15 = make_q('15. 即使身处那些我过去曾应付得很好的场合，我仍然常常对自己没把握')
    q16 = make_q('16. 我常怀疑自己是否有这份天资，能成功地实现我的职业和专业目标')
    q17 = make_q('17. 我比与我年龄、性别相同的大多数人更擅长体育')
    q18 = make_q('18. 我缺少使我成功的一些重要能力')
    q19 = make_q('19. 当我当众讲话时，我常常有把握做到清楚、有效的表达自己的看法')
    q20 = make_q('20. 我真庆幸自己长得漂亮')

    q21 = make_q('21. 我已经意识到，与同我竞争的人相比，我并不是个好学生')
    q22 = make_q('22. 最近几天，我对自己不满意的地方比以往更多')
    q23 = make_q('23. 对体育运动不擅长是我一个很大的缺点')
    q24 = make_q('24. 对我来说，结识一个新朋友是我所盼望的愉快感受')
    q25 = make_q('25. 许多时候，我感到自己不像身边许多人那样有本事')
    q26 = make_q('26. 在晚会或其它许多聚会上，我几乎从未感到过不舒服')
    q27 = make_q('27. 比起大多数人来，我更少怀疑自己的能力')
    q28 = make_q('28. 我在建立爱情关系上，比大多数人因难更多')
    q29 = make_q('29. 今天我比平常对自己的能力更无把握')
    q30 = make_q('30. 令我烦恼的是，我在智力上比不上其它人')

    q31 = make_q('31. 当事情变得糟糕时，我通常相信自己能妥善地处理它们')
    q32 = make_q('32. 我比大多数人更为担心自己在公共场合讲话的能力')
    q33 = make_q('33. 我比我认识的大部分人更自信')
    q34 = make_q('34. 当我考虑继续约会时，我感到紧张或没把握')
    q35 = make_q('35. 大多数人可能会认为我的外表没有吸引力')
    q36 = make_q('36. 当我学一门新课时．我通常可以肯定自己在期末时成绩能处于班上前1/4内')
    q37 = make_q('37. 我像大多数人一样有能力当众讲话')
    q38 = make_q('38. 参加社交聚会时，我常感到笨拙和不自在')
    q39 = make_q('39. 通常情况下，我的爱情生活似乎比大多数人好')
    q40 = make_q('40. 有时我因为不想当众发言而回避上课或做其它事情')

    q41 = make_q('41. 当我必须通过重要的考试或其它专业任务时，我知道自己能行')
    q42 = make_q('42. 我似乎比大多数人更擅长结识新朋友')
    q43 = make_q('43. 我今天比平时更为自信')
    q44 = make_q('44. 我时时避开那些我有可能会与之产生爱情关系的人，因为我在他／她们身边会感到太紧张')
    q45 = make_q('45. 我希望我能改变自己的容貌')
    q46 = make_q('46. 我比大多数人更少担心在公共场合讲话')
    q47 = make_q('47. 现在我感到比乎时更乐观和积极')
    q48 = make_q('48. 对我来说，吸引一个渴幕得到的男女朋友从来不成问题')
    q49 = make_q('49. 假如我更自信一点，我的生活就会好一些')
    q50 = make_q('50. 我追求那些智力上富有挑战性的活动，因为我知道我能比大多数人做得更好')

    q51 = make_q('51. 我能毫无困难地得到许多约会')
    q52 = make_q('52. 我在人群中不能像大多数人那样感到舒服')
    q53 = make_q('53. 今天我比平时对自己更有把握')
    q54 = make_q('54. 要是我长得更好看一些，我会在约会上更成功')

    Academic = models.FloatField()
    Appearance = models.FloatField()
    Athletic = models.FloatField()
    General = models.FloatField()
    Mood = models.FloatField()
    Romance = models.FloatField()
    Social = models.FloatField()
    Speaking = models.FloatField()


# PAGES
class Page1(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10',
                   'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20',
                   'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30',
                   'q31', 'q32', 'q33', 'q34', 'q35', 'q36', 'q37', 'q38', 'q39', 'q40',
                   'q41', 'q42', 'q43', 'q44', 'q45', 'q46', 'q47', 'q48', 'q49', 'q50',
                   'q51', 'q52', 'q53', 'q54']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.Academic = player.q11 + player.q36 + player.q41 + player.q50 - (player.q16 + player.q21 + player.q30)
        player.Appearance = player.q6 + player.q20 - (player.q3 + player.q35 + player.q45 + player.q54)
        player.Athletic = player.q10 + player.q14 + player.q17 - (player.q7 + player.q23)
        player.General = player.q27 + player.q31 + player.q33 - (player.q15 + player.q18 + player.q25 + player.q49)
        player.Mood = player.q5 + player.q43 + player.q47 - (player.q2 + player.q22 + player.q29 + player.q53)
        player.Romance = player.q4 + player.q39 + player.q48 + player.q51 - (player.q28 + player.q34 + player.q44)
        player.Social = player.q1 + player.q24 + player.q26 + player.q42 - (player.q9 + player.q38 - player.q52)
        player.Speaking = player.q12 + player.q19 + player.q37 + player.q46 - (player.q8 + player.q13 + player.q32 + player.q40)


page_sequence = [Page1]
