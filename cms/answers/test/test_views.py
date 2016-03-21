#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from cms.questions.test import BaseTests
from presentations.models import Question, Answer


class AnswerEditViewTests(BaseTests):
    def get_param_list(self):
        """
        Инициализация основных параметров, возвращает список get_response, question, answer, url
        :return: list(response, question, answer, url)
        """
        question = Question.objects.create(text='test?', answers_type='single')
        Answer.objects.create(question=question, position=1, text='test',
                              is_right=True, has_comment=True)
        answer = Answer.objects.create(question=question, position=10, text='test',
                                       is_right=False, has_comment=False)
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': question.id, 'answer': answer.id})
        response = self.client.get(url)
        return response, question, answer, url

    def test_user_is_anonymous(self):
        """
        Тестирует посещение страницы входа неавторизованного пользователя
        проверяем что отправляет на страницу авторизации
        """
        self.client.logout()
        response = self.get_param_list()[0]
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        """
        Тестируем вывод страницы списка вопросов авторизованным пользователем
        с определенными правами(в дальнейшем)
        """
        response = self.get_param_list()[0]
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        """
        Тестируем использование вьюхой нужного нам шаблона
        """
        response = self.get_param_list()[0]
        self.assertTemplateUsed(response, 'cms/answers/edit.html')

    def test_object_in_context(self):
        """
        Тестируем наличие объектов в контексте
        """
        response = self.get_param_list()[0]
        self.assertIn('form', response.context)

    def test_init_form_in_html(self):
        """
        Тестируем инициализацию скрытых значений формы,
        наличие объектов на отрендеренной страничке
        """
        response, question = self.get_param_list()[0:2]
        hidden_input = '<input id="id_question" name="question" type="hidden" value="{}" />'.format(question.id)
        self.assertInHTML(needle=hidden_input, haystack=response.rendered_content)

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        question, answer = self.get_param_list()[1:3]
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': question.id, 'answer': answer.id})
        response = self.client.post(url, {'position': 1000, 'text': 'test edit',
                                          'is_right': True, 'has_comment': True, 'question': question.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        question, answer = self.get_param_list()[1:3]
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': question.id, 'answer': answer.id})
        response = self.client.post(url, {'position': 1000, 'text': 'test edit',
                                          'is_right': True, 'has_comment': True})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        """
        Тестируем POST запрос, отправляем данные в форму.

        Проверяем изменение ответа
        """
        question, _, url = self.get_param_list()[1:4]
        self.client.post(url, {'position': 1000, 'text': 'test edit',
                               'is_right': True, 'has_comment': True, 'question': question.id})
        self.assertEqual(Answer.objects.get(text='test edit').position, 1000)

    def test_name_form_btn_mode_html(self):
        """
        Проверяем верные надписи на форме в шаблоне
        """
        response = self.get_param_list()[0]
        self.assertContains(response, 'Обновить', status_code=200)
        self.assertContains(response, 'Редактирование ответа', status_code=200)

    def test_object_in_html(self):
        """
        Проверяем отображение объекта в шаблоне
        """
        response, question, answer, _ = self.get_param_list()

        self.assertContains(response, question.text, status_code=200)
        self.assertContains(response, answer.position, status_code=200)
        self.assertContains(response, answer.text, status_code=200)
        self.assertContains(response, 'Правильный', status_code=200)
        self.assertContains(response, 'С комментарием', status_code=200)

    def test_nav_button_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        В контексте должны быть следующие навигационные кнопки
        Назад, Удалить
        """
        response = self.get_param_list()[0]
        self.assertIn('back_button', response.context)
        self.assertNotIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertIn('del_button', response.context)

    def test_nav_button_url_in_context(self):
        """
        Тестируем вывод правильных юрлов навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        Назад -> к вопросу, back_url
        /organisation_slug/questions/questions_id/

        Удалить -> к вопросу, del_url
        /organisation_slug/questions/questions_id/answers/answer_id

        """
        response, question, answer, _ = self.get_param_list()
        back_url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': question.id})
        del_url = reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                        'question': question.id, 'answer': answer.id})
        self.assertEqual(back_url, response.context['back_button'])
        self.assertEqual(del_url, response.context['del_button'])

    def test_nav_button_in_html(self):
        """
        Тестируем вывод навигационных кнопок
        Отрисовка кнопок в шаблоне
        """
        response = self.get_param_list()[0]
        self.assertContains(response, 'id="back_button"', status_code=200)
        self.assertContains(response, 'id="del_button"', status_code=200)


class AnswerAddViewTests(BaseTests):
    def get_param_list(self):
        """
        Инициализация основных параметров, возвращает список get_response, question, url
        :return: list(response, question, url)
        """
        question = Question.objects.create(text='test?', answers_type='single')
        Answer.objects.create(question=question, position=1, text='test',
                              is_right=False, has_comment=True)
        Answer.objects.create(question=question, position=2, text='test2',
                              is_right=False, has_comment=False)
        url = reverse('cms:answers-add', kwargs={'organisation': self.organisation.slug,
                                                 'question': question.id})
        response = self.client.get(url)
        return response, question, url

    def test_user_is_anonymous(self):
        """
        Тестирует посещение страницы входа неавторизованного пользователя
        проверяем что отправляет на страницу авторизации
        """
        self.client.logout()
        response = self.get_param_list()[0]
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        """
        Тестируем вывод страницы списка вопросов авторизованным пользователем
        с определенными правами(в дальнейшем)
        """
        response = self.get_param_list()[0]
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        """
        Тестируем использование вьюхой нужного нам шаблона
        """
        response = self.get_param_list()[0]
        self.assertTemplateUsed(response, 'cms/answers/edit.html')

    def test_object_in_context(self):
        """
        Тестируем наличие объектов в контексте
        """
        response = self.get_param_list()[0]
        self.assertIn('form', response.context)

    def test_init_form_in_html(self):
        """
        Тестируем инициализацию скрытых значений формы,
        наличие объектов на отрендеренной страничке
        """
        response, question = self.get_param_list()[0:2]
        hidden_input = '<input id="id_question" name="question" type="hidden" value="{}" />'.format(question.id)
        self.assertInHTML(needle=hidden_input, haystack=response.rendered_content)

    def test_init_form_in_context(self):
        """
        Тестируем наличие вопроса в контексте
        """
        response, question = self.get_param_list()[0:2]
        self.assertEqual(response.context['question'].pk, question.id)

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        _, question, url = self.get_param_list()
        response = self.client.post(url, {'position': 3, 'text': 'new',
                                          'is_right': True, 'has_comment': True, 'question': question.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        _, _, url = self.get_param_list()
        response = self.client.post(url, {'position': 3, 'text': 'new',
                                          'is_right': True, 'has_comment': True})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        """
        Тестируем POST запрос, отправляем данные в форму.

        Проверяем изменение ответа
        """
        _, question, url = self.get_param_list()
        self.client.post(url, {'position': 3, 'text': 'new',
                               'is_right': True, 'has_comment': True, 'question': question.id})
        self.assertEqual(Answer.objects.filter(position=3).count(), 1)
        self.assertEqual(Answer.objects.get(text='new').is_right, True)

    def test_name_form_btn_mode_html(self):
        """
        Проверяем верные надписи на форме в шаблоне
        """
        response = self.get_param_list()[0]
        self.assertContains(response, 'Создать', status_code=200)
        self.assertContains(response, 'Добавление ответа', status_code=200)

    def test_object_in_html(self):
        """
        Проверяем отображение объекта в шаблоне
        """
        response, question, _ = self.get_param_list()
        self.assertContains(response, question.text, status_code=200)
        self.assertContains(response, 'С комментарием', status_code=200)

    def test_nav_button_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        В контексте должны быть следующие навигационные кнопки
        Назад
        """
        response = self.get_param_list()[0]
        self.assertIn('back_button', response.context)
        self.assertNotIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertNotIn('del_button', response.context)

    def test_nav_button_url_in_context(self):
        """
        Тестируем вывод правильных юрлов навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        Назад -> к вопросу, url_back
        /organisation_slug/questions/questions_id/

        """
        response, question, _ = self.get_param_list()
        url_back = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': question.id})
        self.assertEqual(url_back, response.context['back_button'])

    def test_nav_button_in_html(self):
        """
        Тестируем вывод навигационных кнопок
        Отрисовка кнопок в шаблоне
        """
        response = self.get_param_list()[0]
        self.assertContains(response, 'id="back_button"', status_code=200)


class AnswerDeleteViewTests(BaseTests):
    def get_param_list(self):
        """
        Инициализация основных параметров, возвращает список response(post), question, answer, url
        :return: list(response, question, answer, url)
        """
        question = Question.objects.create(text='test?', answers_type='single')
        Answer.objects.create(question=question, position=1, text='test',
                              is_right=False, has_comment=True)
        answer = Answer.objects.create(question=question, position=2, text='test2',
                                       is_right=False, has_comment=False)
        url = reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                    'question': question.id, 'answer': answer.id})
        response = self.client.post(url, {'position': 3, 'text': 'new',
                                          'is_right': True, 'has_comment': True, 'question': question.id})
        return response, question, answer, url

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        response = self.get_param_list()[0]
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        question = self.get_param_list()[1]
        url = reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                    'question': question.id, 'answer': 100})
        response = self.client.post(url)
        self.assertNotEquals(response.status_code, 302)

    def test_delete_object(self):
        """
        Проверям что объект удалился из базы
        """
        question = self.get_param_list()[1]
        self.assertEqual(Answer.objects.filter(question=question).count(), 1)
        self.assertEqual(Answer.objects.filter(position=2, question=question).count(), 0)


class PositionAnswerTest(BaseTests):
        """
        Проверяем функции изминения позиции ответа
        """

        def setUp(self):
            super(PositionAnswerTest, self).setUp()
            self.question = Question.objects.create(text='test?', answers_type='single')
            self.answer_1 = Answer.objects.create(question=self.question, text='1',
                                                  is_right=True, has_comment=True)
            self.answer_2 = Answer.objects.create(question=self.question, text='2',
                                                  is_right=True, has_comment=True)
            self.answer_3 = Answer.objects.create(question=self.question, text='3',
                                                  is_right=True, has_comment=True)

        def test_up_position(self):
            url = reverse('cms:answers-up', kwargs={'organisation': self.organisation.slug,
                                                    'question': self.question.id, 'answer': self.answer_2.id})
            self.client.post(url)
            answer_text_list =[]
            for answer in Answer.objects.all():
                answer_text_list.append(answer.text)
            self.assertEqual(answer_text_list, ['2', '1', '3'])

        def test_down_position(self):
            url = reverse('cms:answers-down', kwargs={'organisation': self.organisation.slug,
                                                      'question': self.question.id, 'answer': self.answer_2.id})
            self.client.post(url)
            answer_text_list = []
            for answer in Answer.objects.all():
                answer_text_list.append(answer.text)
            self.assertEqual(answer_text_list, ['1', '3', '2'])
