# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from user_interface.models import ProjectUser
from presentations.models import Presentation
from presentations.models import Organisation


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        project_user = ProjectUser.objects.get(name='tester')

        org = project_user.organisation  # TODO зачем еще раз делать запрос? у пользователя уже есть организация

        context.update({
            'user': project_user,
            'presentations': Presentation.objects.filter(
                organisation=project_user.organisation
            ),

            'test': org,


        })

        return context
