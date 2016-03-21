#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Manager


class SorterManager(Manager):

    def get_queryset(self):
        return super(SorterManager, self).get_queryset().order_by('position')
