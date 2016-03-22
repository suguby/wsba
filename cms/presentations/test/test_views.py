#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from cms.test import BaseTests
from presentations.models import Presentation


class PresentationListViewTests(BaseTests):

    def setUp(self):
        super(PresentationListViewTests, self).setUp()
        self.presentation = Presentation.objects.create(name='p1', organisation=self.organisation)
        self.presentation_2 = Presentation.objects.create(name='p2', organisation=self.organisation)
        self.url = reverse('cms:presentations-list', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_test_template(self):
        presentations = Presentation.objects.all()
        success_url = reverse('cms:presentations-add', kwargs={'organisation': self.organisation.slug})
        self.assertTemplateUsed(self.response, 'cms/presentations/list.html')
        self.assertEqual(len(presentations), len(self.response.context['object_list']))
        self.assertContains(self.response, self.presentation.name, status_code=200)
        self.assertNotIn('back_button', self.response.context)
        self.assertIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        self.assertEqual(success_url, self.response.context['add_button'])
        self.assertContains(self.response, 'id="add_button"', status_code=200)


class PresentationDetailViewTests(BaseTests):

    def setUp(self):
        super(PresentationDetailViewTests, self).setUp()
        self.presentation = Presentation.objects.create(name='p1', organisation=self.organisation)
        self.url = reverse('cms:presentations-detail', kwargs={'organisation': self.organisation.slug,
                                                               'presentation': self.presentation.id})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_not_get_object(self):
        url_404 = reverse('cms:presentations-detail', kwargs={'organisation': self.organisation.slug,
                                                              'presentation': 100})
        response_404 = self.client.get(url_404)
        self.assertEqual(response_404.status_code, 404)

    def test_template(self):
        url_back = reverse('cms:presentations-list', kwargs={'organisation': self.organisation.slug})
        url_add = reverse('cms:slides-add', kwargs={'organisation': self.organisation.slug,
                                                    'presentation': self.presentation.id})
        url_edit = reverse('cms:presentations-edit', kwargs={'organisation': self.organisation.slug,
                                                             'presentation': self.presentation.id})
        url_delete = reverse('cms:presentations-delete', kwargs={'organisation': self.organisation.slug,
                                                                 'presentation': self.presentation.id})
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertEqual(url_add, self.response.context['add_button'])
        self.assertEqual(url_edit, self.response.context['edit_button'])
        self.assertEqual(url_delete, self.response.context['del_button'])
        self.assertEqual(self.presentation, self.response.context['object'])
        self.assertTemplateUsed(self.response, 'cms/presentations/detail.html')
        self.assertContains(self.response, self.presentation.name, status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertIn('add_button', self.response.context)
        self.assertIn('edit_button', self.response.context)
        self.assertIn('del_button', self.response.context)
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertEqual(url_add, self.response.context['add_button'])
        self.assertEqual(url_edit, self.response.context['edit_button'])
        self.assertEqual(url_delete, self.response.context['del_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)
        self.assertContains(self.response, 'id="add_button"', status_code=200)
        self.assertContains(self.response, 'id="edit_button"', status_code=200)
        self.assertContains(self.response, 'id="del_button"', status_code=200)


class PresentationCreateViewTests(BaseTests):

    def setUp(self):
        super(PresentationCreateViewTests, self).setUp()
        self.presentation = Presentation.objects.create(name='p1', organisation=self.organisation)
        self.url = reverse('cms:presentations-add', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        url_back = reverse('cms:presentations-list', kwargs={'organisation': self.organisation.slug})
        self.assertIn('form', self.response.context)
        self.assertTemplateUsed(self.response, 'cms/presentations/edit.html')
        self.assertContains(self.response, 'Создать', status_code=200)
        self.assertContains(self.response, 'Добавление презентации', status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        url = reverse('cms:presentations-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'name': 'new', 'organisation': self.organisation.id})

        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:presentations-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'name': 'new'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_add_object(self):
        Presentation.objects.create(name='p2', organisation=self.organisation)
        url = reverse('cms:presentations-add', kwargs={'organisation': self.organisation.slug})
        self.client.post(url, {'name': 'new', 'organisation': self.presentation.id})
        self.assertEqual(Presentation.objects.count(), 3)
        self.assertEqual(Presentation.objects.filter(name='new').count(), 1)


class PresentationEditViewTests(BaseTests):

    def setUp(self):
        super(PresentationEditViewTests, self).setUp()
        self.presentation = Presentation.objects.create(name='test', organisation=self.organisation)
        self.url = reverse('cms:presentations-edit', kwargs={'organisation': self.organisation.slug,
                                                             'presentation': self.presentation.id})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertEqual(self.presentation.id, self.response.context['object'].id)
        self.assertTemplateUsed(self.response, 'cms/presentations/edit.html')
        self.assertContains(self.response, 'Обновить', status_code=200)
        self.assertContains(self.response, 'Редактирование презентации', status_code=200)
        self.assertContains(self.response, self.presentation.name, status_code=200)
        self.assertContains(self.response, self.presentation.position, status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        back_url = reverse('cms:presentations-detail', kwargs={'organisation': self.organisation.slug,
                                                               'presentation': self.presentation.id})
        self.assertEqual(back_url, self.response.context['back_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        Presentation.objects.create(name='test123', organisation=self.organisation)
        url = reverse('cms:presentations-edit', kwargs={'organisation': self.organisation.slug,
                                                        'presentation': self.presentation.id})
        response = self.client.post(url, {'name': 'edit test123', 'organisation': self.organisation.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        presentation = Presentation.objects.create(name='test update', organisation=self.organisation)
        url = reverse('cms:presentations-edit', kwargs={'organisation': self.organisation.slug,
                                                        'presentation': presentation.id})
        response = self.client.post(url, {'name': '1'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        presentation = Presentation.objects.create(name='for edit', organisation=self.organisation)
        url = reverse('cms:presentations-edit', kwargs={'organisation': self.organisation.slug,
                                                        'presentation': presentation.id})
        self.client.post(url, {'name': 'edited', 'organisation': self.organisation.id})
        self.assertEqual(Presentation.objects.filter(name='for edit').count(), 0)


class PresentationDeleteViewTests(BaseTests):

    def setUp(self):
        super(PresentationDeleteViewTests, self).setUp()
        self.presentation = Presentation.objects.create(name='test delete p', organisation=self.organisation)
        self.presentation_2 = Presentation.objects.create(name='test delete p2', organisation=self.organisation)
        self.presentation_3 = Presentation.objects.create(name='test delete p3', organisation=self.organisation)
        self.presentation_3 = Presentation.objects.create(name='test delete p4', organisation=self.organisation)
        self.url = reverse('cms:presentations-delete', kwargs={'organisation': self.organisation.slug,
                                                               'presentation': self.presentation_3.id})
        self.response = self.client.post(self.url)

    def test_post_status_valid(self):
        self.assertEquals(self.response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:presentations-delete', kwargs={'organisation': self.organisation.slug, 'presentation': 10})
        response = self.client.post(url)
        self.assertNotEquals(response.status_code, 302)

    def test_delete_object(self):
        self.assertEqual(Presentation.objects.count(), 3)
        self.assertEqual(Presentation.objects.filter(name='test delete p4').count(), 0)
