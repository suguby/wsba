#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from cms.views import BasePresentationsView
from presentations.models import Question, Presentation, Organisation
from django.views.generic import ListView
from django.conf import settings


class PresentationListView(ListView, BasePresentationsView):
    """
    Представление для списка презентаций
    """
    template_name = 'cms/presentations/list.html'
    title = 'Презентации'
    paginate_by = settings.PAGINATE

    def get_queryset(self):
        organisation = Organisation.objects.get(slug=self.kwargs['organisation']) or None
        return Presentation.objects.filter(organisation=organisation).order_by('position')

    def get_context_data(self, **kwargs):
        context = super(PresentationListView, self).get_context_data(**kwargs)
        context['page_kwargs'] = {'organisation': self.kwargs['organisation']}
        return context
