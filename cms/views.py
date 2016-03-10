# -*- coding: utf-8 -*-
from django.http import Http404

from presentations.models import Question, Answer, Organisation

from django.views.generic import ListView


class MainView(ListView):
    model = Question
    template_name = 'cms/index.html'
    title = 'Главаная'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    def get_queryset(self):
        org = self.kwargs['organisation']
        return Question.objects.all()
