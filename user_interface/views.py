# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from user_interface.models import ProjectUser


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context.update({
            'user': ProjectUser.objects.get(name='tester')
        })

        return context
