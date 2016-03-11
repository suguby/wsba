# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import OrganisationIndexView, OrganisationLoginView

urlpatterns = [
    url(r'^login/$', OrganisationLoginView.as_view(), name='organisation_login'),
    url(r'^$', OrganisationIndexView.as_view(), name='organisation_detail'),
]
