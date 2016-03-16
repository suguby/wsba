#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cms.tests import BaseQuestionTestCase
from presentations.models import Question


class CmsQuestionListActionTests(BaseQuestionTestCase):

    def setUp(self):
        super(CmsQuestionListActionTests, self).setUp()
        Question.objects.create(number=2, text='test2')
        self.question_list = Question.objects.all().count()

    def test_question_list(self):
        self.assertEquals(self.question_list, 2)


class CmsQuestionEditActionTests(BaseQuestionTestCase):

    def test_question_edit(self):
        self.question.text = 'new_test'
        self.question.save()
        self.assertEqual(self.question.text, 'new_test')


class CmsQuestionAddActionTests(BaseQuestionTestCase):

    def test_question_add(self):
        question = Question.objects.create(text='new', number=2)
        self.assertEquals(question.text, "new")


class CmsQuestionDeleteViewTests(BaseQuestionTestCase):

    def test_question_delete(self):
        question = Question.objects.get(text='test')
        question.delete()
        self.assertEquals(Question.objects.all().count(), 0)

