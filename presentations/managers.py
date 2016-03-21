#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Manager


class AnswerManager(Manager):

    def get_queryset(self):
        return super(AnswerManager, self).get_queryset().order_by('position')
