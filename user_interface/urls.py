# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import OrganisationIndexView

urlpatterns = [
    url(r'^$', OrganisationIndexView.as_view(), name='organisation_detail'),
]
