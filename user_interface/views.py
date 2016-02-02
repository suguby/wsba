# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from user_interface.models import ProjectUser
from presentations.models import Presentation
from presentations.models import Organisation


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        projectuser = ProjectUser.objects.get(name='tester')

        org = Organisation.objects.get(name=projectuser.organisation.name)

        context.update({
            'user': projectuser,
            'presentations': Presentation.objects.filter(
                organisation=projectuser.organisation
            ),

            'test': org,


        })

        return context
