# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import OrganisationIndexView, ShowPresentation

urlpatterns = [
    url(r'^$', OrganisationIndexView.as_view(), name='organisation_detail'),
    url(r'^presentation/(?P<pk>\d+)/$', ShowPresentation.as_view(), name='show_presentation'),
