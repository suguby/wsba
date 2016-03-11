#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from presentations.models import Organisation


class DashboardView(TemplateView):
    title = 'Панель управления'
    tab = 'dashboard'
    template_name = 'cms/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context