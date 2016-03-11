#!/usr/bin/env python
# -*- coding: utf-8 -*-

from presentations.models import Organisation

from django.views.generic import TemplateView


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

