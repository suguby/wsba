#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from presentations.models import Organisation


class BaseTests(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.organisation = Organisation.objects.create(name='test', slug='test')


class DashboardViewTests(BaseTests):

    def get_response(self):
        # TODO тоже можно в setUp преобразовать
        url = reverse('cms:main', kwargs={'organisation': self.organisation.slug})
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

        self.assertTemplateUsed(response, 'cms/dashboard/index.html')

    def test_objects_in_context(self):
        """
        Тестируем наличие объектов в контексте
        Отправка их в контекст ответа на рендер страницы
        """
        response = self.get_response()

        self.assertEqual(self.organisation, response.context['organisation'])
