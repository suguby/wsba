# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView

from presentations.models import Organisation


class OrganisationLoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(OrganisationLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        organisation = kwargs.get('organisation')
        redirect_to = reverse('organisation_login', kwargs=dict(organisation=organisation))
        redirect_to += '?next={}'.format(request.get_full_path())
        return HttpResponseRedirect(redirect_to=redirect_to)


class OrganisationTemplateView(OrganisationLoginRequiredMixin, TemplateView):

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


class OrganisationLoginView(TemplateView):
    template_name = 'ui/login.html'

    def get_context_data(self, **kwargs):
        aform = AuthenticationForm()
        aform.fields['username'].label = u'Имя пользователя'
        aform.fields['password'].label = u'Пароль'
        context = dict(aform=aform)
        return context

    def post(self, request, *args, **kwargs):
        return 'wow'