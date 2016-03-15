# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from user_interface.models import ProjectUser
from presentations.models import Presentation
from presentations.models import Organisation
from presentations.models import CoreSlide

from presentations.models import Organisation


class OrganisationTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(OrganisationTemplateView, self).get_context_data(**kwargs)
        org_slug = kwargs.get('organisation', '')
        try:
            organisation = Organisation.objects.get(slug=org_slug)
        except Organisation.DoesNotExist:
            raise Http404()
        context.update(organisation=organisation)
        return context


class OrganisationIndexView(OrganisationTemplateView):
    template_name = 'ui/index.html'

    def get_context_data(self, **kwargs):
        context = super(OrganisationIndexView, self).get_context_data(**kwargs)
        project_user = ProjectUser.objects.get(name='tester')
        org = project_user.organisation
        context.update({
            'user': project_user,
            'presentations': Presentation.objects.filter(
                organisation=project_user.organisation
            ),
            'test': org,
        })

        return context


class ShowPresentation(OrganisationTemplateView):
    template_name = 'ui/presentation.html'

    def get_context_data(self, **kwargs):
        context = super(ShowPresentation, self).get_context_data(**kwargs)
        presentation_id = kwargs.get('pk', '')
        try:
            presentation = Presentation.objects.get(id=presentation_id)
        except Organisation.DoesNotExist:
            raise Http404()
        context.update(
            presentation=presentation
        )
        return context


class GoPresentation(OrganisationTemplateView):
    template_name = 'ui/go_presentation.html'

    def get_context_data(self, **kwargs):
        context = super(GoPresentation, self).get_context_data(**kwargs)
        presentation_id = kwargs.get('pk', '')
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            slide = CoreSlide.objects.filter(presentation=presentation)[0]
        except Organisation.DoesNotExist:
            raise Http404()
        context.update(
            presentation=presentation,
            slide=slide
        )
        return context
