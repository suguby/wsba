# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from user_interface.models import ProjectUser
from presentations.models import Presentation, CoreSlide, Organisation
from django.http import HttpResponse
from datetime import datetime, timedelta


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
        context = super().get_context_data(**kwargs)
        project_user = ProjectUser.objects.get(name='tester')



        context.update({
            'user': project_user,
            'presentations': Presentation.objects.filter(organisation=project_user.organisation),

            })
        return context


class PresentationBeginView(OrganisationTemplateView):
    template_name = 'ui/presentation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        presentation_id = kwargs.get('pk', '')


        try:
            presentation = Presentation.objects.get(id=presentation_id)
        except Organisation.DoesNotExist:
            raise Http404()
        start_slide = CoreSlide.objects.filter(presentation_id=presentation_id).order_by('position')[0]
        self.request.session['start'] = True
        self.request.session['time_finish'] = None
        context.update(
                presentation=presentation,
                start_slide=start_slide,
        )
        return context


class PresentationSlideView(OrganisationTemplateView):
    template_name = 'ui/presentation_slide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        presentation_id = kwargs.get('presentation_id', '')
        slide_id = kwargs.get('slide_id', '')
        if self.request.session['start'] == True:
            self.request.session['start'] = False
            self.request.session['time_start'] = datetime.strftime(datetime.now(), "%H:%M:%S")

        try:
            presentation = Presentation.objects.get(id=presentation_id)
            slide = CoreSlide.objects.get(id=slide_id)
        except Organisation.DoesNotExist:
            raise Http404()

        try:
            previous_url = CoreSlide.objects.filter(position__lt=slide.position).order_by('-position')[0].id
        except IndexError:
            previous_url = False

        try:
            next_url = CoreSlide.objects.filter(position__gt=slide.position).order_by('position')[0].id
        except IndexError:
            next_url = False

        context.update(
                presentation=presentation,
                slide=slide,
                len=len(CoreSlide.objects.filter(presentation=presentation_id)),
                next_url=next_url,
                previous_url=previous_url,

        )
        return context


class PresentationDoneView(OrganisationTemplateView):
    template_name = 'ui/presentationdone.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        presentation_id = kwargs.get('pk', '')
        if not self.request.session['time_finish']:
            self.request.session['time_finish'] = datetime.strftime(datetime.now(), "%H:%M:%S")

        st = datetime.strptime(self.request.session['time_start'], "%H:%M:%S")
        fn = datetime.strptime(self.request.session['time_finish'], "%H:%M:%S")
        res = str(fn-st)

        try:
            presentation = Presentation.objects.get(id=presentation_id)
        except Organisation.DoesNotExist:
            raise Http404()

        context.update(
                presentation=presentation,
                st=res,

        )
        return context