#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from cms.presentations.test.test_views import BaseTests
from presentations.models import Presentation, CoreSlide


class SlideEditViewTests(BaseTests):

    def setUp(self):
        super(SlideEditViewTests, self).setUp()
        self.presentation = Presentation.objects.\
            create(name='p1', organisation=self.organisation)
        self.slide = CoreSlide.objects.\
            create(presentation=self.presentation, description='test')
        self.slide_2 = CoreSlide.objects.\
            create(presentation=self.presentation, description='test')
        self.url = reverse('cms:slides_edit',
                           kwargs={'organisation': self.organisation.slug,
                                   'presentation': self.presentation.id,
                                   'slide': self.slide.id})
        self.response = self.client.get(self.url)

    def test_template(self):
        hidden_input = '<input id="id_presentation" ' \
                       'name="presentation" type="hidden" value="{}" />'.\
            format(self.presentation.id)
        back_url = reverse('cms:presentations_detail',
                           kwargs={'organisation': self.organisation.slug,
                                   'presentation': self.presentation.id})
        del_url = reverse('cms:slides_delete',
                          kwargs={'organisation': self.organisation.slug,
                                  'presentation': self.presentation.id,
                                  'slide': self.slide.id})
        self.assertTemplateUsed(self.response, 'cms/slides/edit.html')
        self.assertIn('form', self.response.context)
        self.assertInHTML(needle=hidden_input,
                          haystack=self.response.rendered_content)
        self.assertContains(self.response, 'Обновить', status_code=200)
        self.assertContains(self.response, 'Редактирование слайда',
                            status_code=200)
        self.assertContains(self.response, self. presentation.name,
                            status_code=200)
        self.assertContains(self.response, self.slide.description,
                            status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertIn('del_button', self.response.context)
        self.assertEqual(back_url, self.response.context['back_button'])
        self.assertEqual(del_url, self.response.context['del_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)
        self.assertContains(self.response, 'id="del_button"', status_code=200)

    def test_post_status_valid(self):
        url = reverse('cms:slides_edit',
                      kwargs={'organisation': self.organisation.slug,
                              'presentation': self.presentation.id,
                              'slide': self.slide.id})
        response = self.client.post(url,
                                    {'description': 'description',
                                     'presentation': self.presentation.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:slides_edit',
                      kwargs={'organisation': self.organisation.slug,
                              'presentation': self.presentation.id,
                              'slide': self.slide.id})
        response = self.client.post(url, {'description': 'test edit'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        self.client.post(self.url, {'description': 'test edit',
                                    'presentation': self.presentation.id})
        self.assertEqual(CoreSlide.objects.
                         filter(description='test edit').count(), 1)


class CoreSlideAddViewTests(BaseTests):

    def setUp(self):
        super(CoreSlideAddViewTests, self).setUp()
        self.presentation = Presentation.objects.\
            create(name='p1', organisation=self.organisation)
        self.slide = CoreSlide.objects.\
            create(presentation=self.presentation, description='test')
        self.slide_2 = CoreSlide.objects.\
            create(presentation=self.presentation, description='test2')
        self.url = reverse('cms:slides_add',
                           kwargs={'organisation': self.organisation.slug,
                                   'presentation': self.presentation.id})
        self.response = self.client.get(self.url)

    def test_template(self):
        hidden_input = '<input id="id_presentation"' \
                       ' name="presentation" type="hidden" value="{}" />'.\
            format(self.presentation.id)
        url_back = reverse('cms:presentations_detail',
                           kwargs={'organisation': self.organisation.slug,
                                   'presentation': self.presentation.id})

        self.assertTemplateUsed(self.response, 'cms/slides/edit.html')
        self.assertIn('form', self.response.context)
        self.assertInHTML(needle=hidden_input,
                          haystack=self.response.rendered_content)
        self.assertEqual(self.response.context['presentation'].pk,
                         self.presentation.id)
        self.assertContains(self.response, 'Создать', status_code=200)
        self.assertContains(self.response, 'Добавление слайда',
                            status_code=200)
        self.assertContains(self.response, self.presentation.name,
                            status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        response = self.client.post(self.url, {'description': 'test edit',
                                    'presentation': self.presentation.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        response = self.client.post(self.url, {'description': 'test edit'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        self.client.post(self.url, {'description': '12345',
                                    'presentation': self.presentation.id})
        self.assertEqual(CoreSlide.objects.
                         filter(description='12345').count(), 1)


class CoreSlideDeleteViewTests(BaseTests):

    def setUp(self):
        super(CoreSlideDeleteViewTests, self).setUp()
        self.presentation = Presentation.objects.\
            create(name='p1', organisation=self.organisation)
        self.slide = CoreSlide.objects.\
            create(presentation=self.presentation, description='test1')
        self.slide_2 = CoreSlide.objects.\
            create(presentation=self.presentation, description='test2')
        self.url = reverse('cms:slides_delete',
                           kwargs={'organisation': self.organisation.slug,
                                   'presentation': self.presentation.id,
                                   'slide': self.slide.id})
        self.response = \
            self.client.post(self.url, {'position': 2, 'description': 'test2',
                                        'presentation': self.presentation.id})

    def test_post_status_valid(self):
        self.assertEquals(self.response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:slides_delete',
                      kwargs={'organisation': self.organisation.slug,
                              'presentation': self.presentation.id,
                              'slide': 100})
        response = self.client.post(url)
        self.assertNotEquals(response.status_code, 302)

    def test_delete_object(self):
        self.assertEqual(CoreSlide.objects.
                         filter(presentation=self.presentation).count(), 1)
        self.assertEqual(CoreSlide.objects.
                         filter(position=2, description='test1').count(), 0)


class PositionSlideTest(BaseTests):

    def setUp(self):
        super(PositionSlideTest, self).setUp()
        self.presentation = Presentation.objects.\
            create(name='p1', organisation=self.organisation)
        self.slide = CoreSlide.objects.\
            create(presentation=self.presentation, description='test1')
        self.slide_2 = CoreSlide.objects.\
            create(presentation=self.presentation, description='test2')

    def test_up_position(self):
        url = reverse('cms:slides_up',
                      kwargs={'organisation': self.organisation.slug,
                              'presentation': self.presentation.id,
                              'slide': self.slide_2.id})
        self.client.post(url)
        slides_list = []
        for slide in CoreSlide.objects.all():
            slides_list.append(slide.description)
        self.assertEqual(slides_list, ['test2', 'test1'])

    def test_down_position(self):
        url = reverse('cms:slides_up',
                      kwargs={'organisation': self.organisation.slug,
                              'presentation': self.presentation.id,
                              'slide': self.slide_2.id})
        self.client.post(url)
        slides_list = []
        for slide in CoreSlide.objects.all():
            slides_list.append(slide.description)
        self.assertEqual(slides_list, ['test2', 'test1'])
