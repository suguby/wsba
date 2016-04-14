# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from presentations.models import Presentation, CoreSlide, Organisation
from presentations.views import slide_question_context
from user_interface.models import ProjectUser, UserPresentation


class OrganisationLoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(OrganisationLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        redirect_to = reverse('login')
        redirect_to += '?next={}'.format(request.get_full_path())
        return HttpResponseRedirect(redirect_to=redirect_to)


class OrganisationTemplateView(OrganisationLoginRequiredMixin, TemplateView):

    def render_to_response(self, context, **response_kwargs):
        response = super(OrganisationTemplateView, self).render_to_response(context, **response_kwargs)
        response.set_cookie("success","success")
        return response

    def get_context_data(self, **kwargs):
        context = super(OrganisationTemplateView, self).get_context_data(**kwargs)
        org_slug = kwargs.get('organisation', '')
        try:
            organisation = Organisation.objects.get(slug=org_slug)
        except Organisation.DoesNotExist:
            raise Http404()
        self.request.session['user'] = self.request.user.username

        context.update(
                organisation=organisation,
                project_user=self.request.user,
        )
        return context


class OrganisationIndexView(OrganisationTemplateView):
    template_name = 'ui/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_user = ProjectUser.objects.get(id=self.request.user.id)

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
        # TODO здесь падает если у презентации нету слайдов
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
            # TODO высушить
            previous_url = reverse('presentation_slide',
                               kwargs=dict(
                                    organisation=presentation.organisation.slug,
                                    presentation_id=presentation.id,
                                    slide_id=CoreSlide.objects.filter(position__lt=slide.position).order_by('-position')[0].id
                               )
                            )
        except IndexError:
            previous_url = False

        try:
            next_url = reverse('presentation_slide',
                               kwargs=dict(
                                    organisation=presentation.organisation.slug,
                                    presentation_id=presentation.id,
                                   #  TODO фильтровать по презентации !!!
                                    slide_id=CoreSlide.objects.filter(position__gt=slide.position).order_by('position')[0].id
                               )
                            )
        except IndexError:
            next_url = False

        last_url = reverse('presentationdone', kwargs=dict(organisation=presentation.organisation.slug, pk=presentation.id))

        context.update(
                presentation=presentation,
                slide=slide,
                len=len(CoreSlide.objects.filter(presentation=presentation_id)),
                next_url=next_url,
                previous_url=previous_url,
                last_url=last_url,
        )
        if slide.question:
            slide_question_context(context=context, kwargs=kwargs)

        return context


class PresentationDoneView(OrganisationTemplateView):
    template_name = 'ui/presentationdone.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        presentation_id = kwargs.get('pk', '')
        if not self.request.session['time_finish']:
            self.request.session['time_finish'] = datetime.strftime(datetime.now(), "%H:%M:%S")

        res = str(
                datetime.strptime(self.request.session['time_finish'], "%H:%M:%S") - datetime.strptime(
                        self.request.session['time_start'], "%H:%M:%S")
        )

        try:
            presentation = Presentation.objects.get(id=presentation_id)
        except Organisation.DoesNotExist:
            raise Http404()

        done = UserPresentation.objects.create(
                user=ProjectUser.objects.get(name=self.request.session['user']),
                presentation=presentation,
                passage_time=res,
        )
        context.update(
                presentation=presentation,
                st=res,

        )
        return context


