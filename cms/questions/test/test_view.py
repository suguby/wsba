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

    def test_objects_in_context(self):
        """
        Тестируем наличие объектов в контексте
        Отправка их в контекст ответа на рендер страницы
        """
        Question.objects.create(text='test', answers_type='single')
        Question.objects.create(text='test2', answers_type='single')
        question = Question.objects.create(text='test3', answers_type='single')
        questions = Question.objects.all()
        success_url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.get_response()

        self.assertTemplateUsed(response, 'cms/questions/list.html')
        self.assertEqual(len(questions), len(response.context['object_list']))
        self.assertContains(response, question.text, status_code=200)

        self.assertNotIn('back_button', response.context)
        self.assertIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertNotIn('del_button', response.context)

        self.assertEqual(success_url, response.context['add_button'])
        self.assertContains(response, 'id="add_button"', status_code=200)


class QuestionDetailViewTests(BaseTests):

    def get_response_and_question(self):
        question = Question.objects.create(text='test?', answers_type='single')
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

    def test_object_in_context(self):
        """
        Тестируем наличие вопроса в контексте
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
        self.assertEqual(question, response.context['object'])
        self.assertTemplateUsed(response, 'cms/questions/detail.html')
        self.assertContains(response, question.text, status_code=200)

        self.assertIn('back_button', response.context)
        self.assertIn('add_button', response.context)
        self.assertIn('edit_button', response.context)
        self.assertIn('del_button', response.context)

        self.assertEqual(url_back, response.context['back_button'])
        self.assertEqual(url_add, response.context['add_button'])
        self.assertEqual(url_edit, response.context['edit_button'])
        self.assertEqual(url_delete, response.context['del_button'])

        self.assertContains(response, 'id="back_button"', status_code=200)
        self.assertContains(response, 'id="add_button"', status_code=200)
        self.assertContains(response, 'id="edit_button"', status_code=200)
        self.assertContains(response, 'id="del_button"', status_code=200)


class QuestionCreateViewTests(BaseTests):

    def get_response(self):
        Question.objects.create(text='test update', answers_type='single')
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

    def test_object_in_context(self):
        """
        Тестируем наличие объектов в контексте
        """
        response = self.get_response()
        url_back = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'cms/questions/edit.html')
        self.assertContains(response, 'Создать', status_code=200)
        self.assertContains(response, 'Добавление вопроса', status_code=200)

        self.assertIn('back_button', response.context)
        self.assertNotIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertNotIn('del_button', response.context)

        self.assertEqual(url_back, response.context['back_button'])

        self.assertContains(response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'text': 'new_question', 'answers_type': 'multi'})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'text': 'new_question'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_add_object(self):
        """
        Тестируем POST запрос, отправляем данные в форму.

        Проверяем добавился ли вопрос в базу, при налии одного вопроса добавляем
        еще один и сравниваем их количество

        Ищем наш объект в базе и проверяем его имя сходится ли оно с введенными данными в форму
        """
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.client.post(url, {'text': 'new_question', 'answers_type': 'multi'})
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.filter(text='new_question').count(), 1)


class QuestionEditViewTests(BaseTests):

    def get_response_and_question(self):
        question = Question.objects.create(text='test update', answers_type='single')
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

    def test_object_in_context(self):
        """
        Тестируем наличие объектов в контексте
        """
        question, response = self.get_response_and_question()
        self.assertEqual(question.id, response.context['object'].id)
        self.assertTemplateUsed(response, 'cms/questions/edit.html')
        self.assertContains(response, 'Обновить', status_code=200)
        self.assertContains(response, 'Редактирование вопроса', status_code=200)

        self.assertContains(response, question.text, status_code=200)
        self.assertContains(response, question.answers_type, status_code=200)

        self.assertIn('back_button', response.context)
        self.assertNotIn('add_button', response.context)
        self.assertNotIn('edit_button', response.context)
        self.assertNotIn('del_button', response.context)

        back_url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': question.id})
        self.assertEqual(back_url, response.context['back_button'])
        self.assertContains(response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        question = Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response = self.client.post(url, {'text': 'edit question', 'answers_type': 'multi'})

        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при невалидных данных не проходит ли редирект
        """
        question = Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response = self.client.post(url, {'text': '1'})

        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        """
        Тестируем POST запрос, отправляем данные в форму.

        Проверяем изменение вопроса
        """
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.client.post(url, {'text': 'edit question', 'answers_type': 'multi'})
        self.assertEqual(Question.objects.filter(answers_type='test update').count(), 0)


class QuestionDeleteViewTests(BaseTests):

    # TODO: Реализовать: Удаление пользователем, не имеющих соответствующих прав

    def test_post_status_valid(self):
        """
        Тестируем POST запрос, отправляем данные в форму.
        Проверяем при валидных данных проходит ли редирект
        """
        question = Question.objects.create(text='test delete 3', answers_type='single')
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
        Question.objects.create(text='test delete', answers_type='single')
        Question.objects.create(text='test delete 2', answers_type='single')
        question = Question.objects.create(text='test delete 3', answers_type='single')
        url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        self.client.post(url)

        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.filter(text='test delete 3').count(), 0)
