# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import OrganisationIndexView, ShowPresentation, GoPresentation

urlpatterns = [
    url(r'^$', OrganisationIndexView.as_view(), name='organisation_detail'),
    url(r'^presentation/(?P<pk>\d+)/$', ShowPresentation.as_view(), name='show_presentation'),
    url(r'^presentation/(?P<presentation_id>\d+)/slides/(?P<slide_id>\d+)$', GoPresentation.as_view(), name='go_presentation'),
]
