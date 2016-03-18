#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from presentations.models import Organisation, Question
from django.conf import settings


class BaseTests(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.organisation = Organisation.objects.create(name='test', slug='test')


class QuestionListViewTests(BaseTests):

    def get_response(self):
        url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        response = self.client.get(url)
        return response

    def test_user_is_anonymous(self):
        """
        Тестирует посещение страницы входа неавторизованного пользователя
        проверяем что отправляет на страницу авторизации
        url которой прописан в настройках settings параметр LOGIN_URL
        на стронице логин происходит тоже редирект поэтому и status_code=302, target_status_code=302
        """
        self.client.logout()
        response = self.get_response()
        redirect_url = settings.LOGIN_URL + '?next={}'.format(reverse('cms:questions-list',
                                                                      kwargs={'organisation': self.organisation.slug}))
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=302)
        self.assertIn(settings.LOGIN_URL, response.url)
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        """
        Тестируем вывод страницы списка вопросов авторизованным пользователем
        с определенными правами(в дальнейшем)
        """
        response = self.get_response()

        self.assertEquals(response.status_code, 200)

    def test_template(self):
        """
        Тестируем использование вьюхой нужного нам шаблона
        """
        response = self.get_response()

        self.assertTemplateUsed(response, 'cms/questions/list.html')

    def test_objects_in_context(self):
        """
        Тестируем наличие объектов в контексте
        Отправка их в контекст ответа на рендер страницы
        """
        Question.objects.create(number=1, text='test', answers_type='single')
        Question.objects.create(number=2, text='test2', answers_type='single')
        Question.objects.create(number=3, text='test3', answers_type='single')
        questions = Question.objects.all()
        response = self.get_response()

        self.assertEqual(len(questions), len(response.context['object_list']))

    def test_html(self):
        """
        Тестируем вывод наших данных в шаблоне
        """
        url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        question = Question.objects.create(number=1, text='test', answers_type='single')
        response = self.client.get(url)

        self.assertContains(response, question.text, status_code=200)

    def test_nav_button_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы
        """
        response = self.get_response()

        self.assertNotIn('back_button', response.context)
        self.assertIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertNotIn('del_button', response.context)

    def test_nav_button_url_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы
        """
        url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        success_url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.get(url)

        self.assertEqual(success_url, response.context['add_button'])

    def test_nav_button_in_html(self):
        """
        Тестируем вывод навигационных кнопок
        Отрисовка кнопок в шаблоне
        """
        response = self.get_response()

        self.assertContains(response, 'id="add_button"', status_code=200)


class QuestionDetailViewTests(BaseTests):

    def get_response_and_question(self):
        question = Question.objects.create(number=2, text='test?', answers_type='single')
        url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                      'question': question.id})
        response = self.client.get(url)
        return question, response

    def test_user_is_anonymous(self):
        """
        Тестирует посещение страницы входа неавторизованного пользователя
        проверяем что отправляет на страницу авторизации
        """
        self.client.logout()
        question, response = self.get_response_and_question()
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        """
        Тестируем вывод страницы списка вопросов авторизованным пользователем
        с определенными правами(в дальнейшем)
        """
        question, response = self.get_response_and_question()
        self.assertEquals(response.status_code, 200)

    def test_not_get_object(self):
        """
        Тестируем вывод страницы с не существующим обектом, должна вернуться ошибка 404
        """
        url_404 = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                          'question': 100})
        response_404 = self.client.get(url_404)

        self.assertEqual(response_404.status_code, 404)

    def test_template(self):
        """
        Тестируем использование вьюхой нужного нам шаблона
        """
        question, response = self.get_response_and_question()
        self.assertTemplateUsed(response, 'cms/questions/detail.html')

    def test_object_in_context(self):
        """
        Тестируем наличие вопроса в контексте
        """
        question, response = self.get_response_and_question()
        self.assertEqual(question, response.context['object'])

    def test_object_in_html(self):
        """
        Тестируем вывод вопроса в шаблон
        """
        question, response = self.get_response_and_question()
        self.assertContains(response, question.number, status_code=200)
        self.assertContains(response, question.text, status_code=200)

    def test_nav_button_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        В контексте должны быть все навигационные кнопки
        Назад, Добавить, Редактировать, Удалить
        """
        question, response = self.get_response_and_question()

        self.assertIn('back_button', response.context)
        self.assertIn('add_button', response.context)
        self.assertIn('edit_button', response.context)
        self.assertIn('del_button', response.context)

    def test_nav_button_url_in_context(self):
        """
        Тестируем вывод правильных юрлов навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        Назад -> к списку вопросов, url_back
        /organisation_slug/questions/

        Добавить -> добавить ответ, url_add
        /organisation_slug/questions/new

        Редактировать -> редактировать ответ, url_edit
        /organisation_slug/questions/question_id/edit

        Удалить -> удалить ответ, url_delete
        /organisation_slug/questions/question_id/delete
        """
        question, response = self.get_response_and_question()
        url_back = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        url_add = reverse('cms:answers-add', kwargs={'organisation': self.organisation.slug,
                                                     'question': question.id})
        url_edit = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                         'question': question.id})
        url_delete = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug,
                                                             'question': question.id})
        self.assertEqual(url_back, response.context['back_button'])
        self.assertEqual(url_add, response.context['add_button'])
        self.assertEqual(url_edit, response.context['edit_button'])
        self.assertEqual(url_delete, response.context['del_button'])

    def test_nav_button_in_html(self):
        """
        Тестируем вывод навигационных кнопок
        Отрисовка кнопок в шаблоне
        """
        question, response = self.get_response_and_question()
        self.assertContains(response, 'id="back_button"', status_code=200)
        self.assertContains(response, 'id="add_button"', status_code=200)
        self.assertContains(response, 'id="edit_button"', status_code=200)
        self.assertContains(response, 'id="del_button"', status_code=200)


class QuestionCreateViewTests(BaseTests):

    def get_response(self):
        Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.get(url)
        return response

    def test_user_is_anonymous(self):
        """
        Тестирует посещение страницы входа неавторизованного пользователя
        проверяем что отправляет на страницу авторизации
        """
        self.client.logout()
        response = self.get_response()
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        """
        Тестируем вывод страницы списка вопросов авторизованным пользователем
        с определенными правами(в дальнейшем)
        """
        response = self.get_response()
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        """
        Тестируем использование вьюхой нужного нам шаблона
        """
        response = self.get_response()
        self.assertTemplateUsed(response, 'cms/questions/edit.html')

    def test_object_in_context(self):
        """
        Тестируем наличие объектов в контексте
        """
        response = self.get_response()
        self.assertIn('form', response.context)

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'number': 1, 'text': 'new_question', 'answers_type': 'multi'})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'number': 1, 'text': 'new_question'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_add_object(self):
        """
        Тестируем POST запрос, отправляем данные в форму.

        Проверяем добавился ли вопрос в базу, при налии одного вопроса добавляем
        еще один и сравниваем их количество

        Ищем наш объект в базе и проверяем его имя сходится ли оно с введенными данными в форму
        """
        Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.client.post(url, {'number': 1, 'text': 'new_question', 'answers_type': 'multi'})
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.get(number=1).text, 'new_question')

    def test_name_form_btn_mode_html(self):
        """
        Проверяем верные надписи на форме в шаблоне
        """
        response = self.get_response()
        self.assertContains(response, 'Создать', status_code=200)
        self.assertContains(response, 'Добавление вопроса', status_code=200)

    def test_nav_button_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        В контексте должны быть следующие навигационные кнопки
        Назад
        """
        response = self.get_response()
        self.assertIn('back_button', response.context)
        self.assertNotIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertNotIn('del_button', response.context)

    def test_nav_button_url_in_context(self):
        """
        Тестируем вывод правильных юрлов навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        Назад -> к списку вопросов, url_back
        /organisation_slug/questions/

        """
        response = self.get_response()
        url_back = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.assertEqual(url_back, response.context['back_button'])

    def test_nav_button_in_html(self):
        """
        Тестируем вывод навигационных кнопок
        Отрисовка кнопок в шаблоне
        """
        response = self.get_response()
        self.assertContains(response, 'id="back_button"', status_code=200)


class QuestionEditViewTests(BaseTests):

    def get_response_and_question(self):
        question = Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response = self.client.get(url)
        return question, response

    def test_user_is_anonymous(self):
        """
        Тестирует посещение страницы входа неавторизованного пользователя
        проверяем что отправляет на страницу авторизации
        """
        self.client.logout()
        question, response = self.get_response_and_question()
        self.assertEqual(response.status_code, 302)

    def test_user_is_authenticated(self):
        """
        Тестируем вывод страницы списка вопросов авторизованным пользователем
        с определенными правами(в дальнейшем)
        """
        question, response = self.get_response_and_question()
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        """
        Тестируем использование вьюхой нужного нам шаблона
        """
        question, response = self.get_response_and_question()

        self.assertTemplateUsed(response, 'cms/questions/edit.html')

    def test_object_in_context(self):
        """
        Тестируем наличие объектов в контексте
        """
        question, response = self.get_response_and_question()
        self.assertEqual(question.id, response.context['object'].id)

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        question = Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response = self.client.post(url, {'number': 1000, 'text': 'edit question', 'answers_type': 'multi'})

        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        question = Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response = self.client.post(url, {'number': 1000, 'text': ''})

        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        """
        Тестируем POST запрос, отправляем данные в форму.

        Проверяем изменение вопроса
        """
        Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.client.post(url, {'number': 1000, 'text': 'edit question', 'answers_type': 'multi'})
        self.assertEqual(Question.objects.get(text='edit question').number, 1000)

    def test_name_form_btn_mode_html(self):
        """
        Проверяем верные надписи на форме в шаблоне
        """
        question, response = self.get_response_and_question()
        self.assertContains(response, 'Обновить', status_code=200)
        self.assertContains(response, 'Редактирование вопроса', status_code=200)

    def test_object_in_html(self):
        """
        Проверяем отображение объекта в шаблоне
        """
        question, response = self.get_response_and_question()
        self.assertContains(response, question.number, status_code=200)
        self.assertContains(response, question.text, status_code=200)
        self.assertContains(response, question.answers_type, status_code=200)

    def test_nav_button_in_context(self):
        """
        Тестируем вывод навигационных кнопок
        Отправка их в контекст ответа на рендер страницы

        В контексте должны быть следующие навигационные кнопки
        Назад
        """
        question, response = self.get_response_and_question()
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
        question = Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        back_url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': question.id})
        response = self.client.get(url)
        self.assertEqual(back_url, response.context['back_button'])

    def test_nav_button_in_html(self):
        """
        Тестируем вывод навигационных кнопок
        Отрисовка кнопок в шаблоне
        """
        question, response = self.get_response_and_question()
        self.assertContains(response, 'id="back_button"', status_code=200)


class QuestionDeleteViewTests(BaseTests):

    # TODO: Реализовать: Удаление пользователем, не имеющих соответствующих прав

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        question = Question.objects.create(number=3, text='test delete 3', answers_type='single')
        url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug,
                                                      'question': question.id})
        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug, 'question': 10})
        response = self.client.post(url)

        self.assertNotEquals(response.status_code, 302)

    def test_delete_object(self):
        """
        Проверям что объект удалился из базы
        """
        Question.objects.create(number=1, text='test delete', answers_type='single')
        Question.objects.create(number=2, text='test delete 2', answers_type='single')
        question = Question.objects.create(number=3, text='test delete 3', answers_type='single')
        url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        self.client.post(url)

        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.filter(number=3).count(), 0)
