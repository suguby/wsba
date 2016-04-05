# -*- coding: utf-8 -*-
import random

from django.core.management import BaseCommand

from presentations.models import Organisation, Presentation, CoreSlide, Question, Answer


class DbFiller:

    TEXTS = (
    """
    Ретардация отражает индивидуальный гомеостаз. Самонаблюдение решает эллиптический аутизм.
    Красноватая звездочка, иcходя из того, что непоследовательно отражает далекий гештальт.
    """,
    """
    Когда речь идет о галактиках, восприятие выбирает депрессивный комплекс.
    Расстояния планет от Солнца возрастают приблизительно в геометрической прогрессии
    (правило Тициуса — Боде): г = 0,4 + 0,3 · 2n (а.е.), где роль вероятна.
    Этот концепт элиминирует концепт «нормального», однако керн выбирает
    экваториальный экватор. Летучая Рыба, несмотря на внешние воздействия,
    вызывает узел. Самонаблюдение оценивает болид .
    """,
    """
    Кульминация отталкивает психоанализ, хотя для имеющих глаза-телескопы туманность Андромеды
    показалась бы на небе величиной с треть ковша Большой Медведицы. Мышление, как бы это ни казалось парадоксальным,
    однородно вызывает филогенез. Астероид отражает оппортунический Южный Треугольник,
    о чем и писал А.Маслоу в своей работе "Мотивация и личность"
    Доминантсептаккорд добросовестно использует акцепт. Полимодальная организация реквизирует шоу-бизнес,
    в таких условиях можно спокойно выпускать пластинки раз в три года. Концессия противозаконна.
    Индоссамент опротестован. В соответствии со сложившейся правоприменительной практикой конфиденциальность
    синхронно гарантирует гарантийный субъект. Звукосниматель объективно добросовестно использует ничтожный цикл.
    Банкротство гарантирует конфиденциальный канал. Аллюзийно-полистилистическая композиция принципиально
    экспортирует open-air. Фрахтование формирует доминантсептаккорд. Ретро имитирует соноропериод.
    Адажио деформирует причиненный ущерб. Разлом страхует причиненный ущерб, включая и гряды Чернова, Чернышева и др.
    Из комментариев экспертов, анализирующих законопроект, не всегда можно определить, когда именно океаническое ложе
    обогащает апериодический предпринимательский риск. Арпеджио поручает конструктивный шельф, это и есть одномоментная
    вертикаль в сверхмногоголосной полифонической ткани. Согласно теории устойчивости движения авгит позволяет
    пренебречь колебаниями корпуса, хотя этого в любом случае требует биокосный экваториальный момент.
    Тальвег, в первом приближении, дает меандр, что не имеет аналогов в англо-саксонской правовой системе.
    Исключая малые величины из уравнений, погрешность относительно лицензирует флэнжер. Момент сил неустойчив.
    Внутреннее кольцо позволяет исключить из рассмотрения пелагический гарант. Наследование последовательно.
    Помимо права собственности и иных вещных прав, Указ своевременно исполняет цокольный субъект.
    Рефрен утолщен. Кластерное вибрато поступательно. В соответствии с законами сохранения энергии,
    гипергенный минерал анизотропно формирует уходящий товарный кредит, за счет чего увеличивается мощность коры
    под многими хребтами. Несомненный интерес представляет и тот факт, что гипнотический рифф вызывает жидкий акцепт.
    В самом общем случае магма отчетливо и полно арендует огненный пояс. Цикл использует оз.
    """,
    )
    QUESTIONS = ('Кто виноват?', 'Что делать?', 'Доколе?',
                 'Поручает ли арпеджио конструктивный шельф и одномоментная вертикаль в сверхмногоголосной полифонической ткани ???',
                 'Полнолуние косвенно. Open-air, на первый взгляд, прочно выстраивает диссонансный аккорд, Плутон не входит в эту классификацию. Приливное трение, в первом приближении, регрессийно имеет конструктивный цикл. В связи с этим нужно подчеркнуть, что газопылевое облако многопланово заканчивает космический перигелий, выслеживая яркие, броские образования ???',
                 )
    ANSWERS = ('Да', 'Нет', 'Не знаю', 'кто здесь?',
               'Юлианская дата выслеживает лайн-ап.',
               'Спектральный класс начинает спектральный класс. ',
               'Приливное трение, в первом приближении, регрессийно имеет конструктивный цикл. ',
               'Очевидно, что асинхронное ритмическое поле ненаблюдаемо.',
               'Ощущение мономерности ритмического движения возникает, как правило, в условиях темповой стабильности',
               'Пpотопланетное облако, в первом приближении, использует аргумент перигелия.',
               )
    ANSWER_TYPE = [x[0] for x in Question.ANSWER_TYPE]

    def __init__(self, options):
        self.options = options
        self.organisation = None
        self.presentations = None
        self.slides = None
        self.question_count = self.anwsers_count = 0

    def _get_option_range(self, name, default='3-5'):
        params = self.options.get(name, default).split('-')
        try:
            a, b = params
        except ValueError:
            a = b = params[0]
        return range(random.randint(int(a), int(b)))

    def run(self):
        if self.options.get('clear', False):
            self._clean_db()
        self.question_count = self.anwsers_count = 0
        self.organisation, created = Organisation.objects.get_or_create(name='Икеа', slug='ikea')
        self.presentations = self._get_presentations()
        print('Added {} presentations'.format(len(self.presentations)))
        self.slides = self._get_slides()
        print('Added {} slides'.format(len(self.slides)))
        self._append_questions()
        print('Added {} questions with {} anwsers'.format(self.question_count, self.anwsers_count))

    def _get_presentations(self):
        presentations = []
        for i in self._get_option_range('presentations'):
            pr, created = Presentation.objects.get_or_create(
                organisation=self.organisation,
                name='Презентация {}'.format(i),
                defaults=dict(
                    slug='presentation_{}'.format(i),
                    position=i,
                )
            )
            presentations.append(pr)
        return presentations

    def _get_slides(self):
        slides = []
        for pr in self.presentations:
            for i in self._get_option_range('slides'):
                slide, created = CoreSlide.objects.get_or_create(
                    presentation=pr,
                    description=random.choice(self.TEXTS),
                    defaults=dict(
                        image='my_pic.jpg',
                        slug='slide_{}'.format(i),
                        position=i,
                    )
                )
                slides.append(slide)
        return slides

    def _append_questions(self):
        for i, slide in enumerate(self.slides):
            if random.randint(1, 10) == 7:
                # without question
                continue
            question_text = random.choice(self.QUESTIONS)
            question, created = Question.objects.get_or_create(
                text=question_text,
                defaults=dict(
                    number=i,
                    answers_type=random.choice(self.ANSWER_TYPE)
                )
            )
            self.question_count += 1
            for j in self._get_option_range('answers'):
                Answer.objects.get_or_create(
                    question=question,
                    text=random.choice(self.ANSWERS),
                    defaults=dict(
                        variant_number=j,
                        is_right=random.choice([True, False]),
                        has_comment=random.choice([True, False]),
                    )
                )
                self.anwsers_count += 1
            slide.question = question
            slide.save()

    def _clean_db(self):
        Answer.objects.all().delete()
        Question.objects.all().delete()
        CoreSlide.objects.all().delete()
        Presentation.objects.all().delete()
        print('Database cleaned')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--clear',
                            action='store_true',
                            dest='clear',
                            default=False,
                            help='очистить предварительно базу')
        parser.add_argument('--presentations',
                            action='store',
                            dest='presentations',
                            default='3-5',
                            help='сколько создавать презентаций (можно диапазоном)')
        parser.add_argument('--slides',
                            action='store',
                            dest='slides',
                            default='3-5',
                            help='сколько создавать слайдов (можно диапазоном)')
        parser.add_argument('--answers',
                            action='store',
                            dest='answers',
                            default='3-5',
                            help='сколько создавать вариантов ответов (можно диапазоном)')

    def handle(self, *args, **options):
        runner = DbFiller(options=options)
        runner.run()
