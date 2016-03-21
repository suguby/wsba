#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Manager


class PositionManager(Manager):

    def sorted(self):
        return self.order_by('position')
