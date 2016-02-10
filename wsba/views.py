#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView

from presentations.models import Organisation


class WsbaTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(WsbaTemplateView, self).get_context_data(**kwargs)
        org_slug = kwargs.get('organisation', '')
        try:
            organisation = Organisation.objects.get(slug=org_slug)
        except Organisation.DoesNotExist:
            raise Http404()
        context.update(organisation=organisation)
        return context


class IndexView(TemplateView):
    template_name = 'index.html'

