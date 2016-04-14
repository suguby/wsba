# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (OrganisationIndexView, PresentationBeginView, PresentationSlideView,
                    PresentationDoneView, OrganisationLoginView, )

urlpatterns = [
    url(r'^login/$', OrganisationLoginView.as_view(), name='organisation_login'),
    url(r'^$', OrganisationIndexView.as_view(), name='organisation_detail'),
    url(r'^presentation/(?P<pk>\d+)/$',  # TODO изменить на presentation_id
        PresentationBeginView.as_view(), name='presentation_begin'),
    url(r'^presentation/(?P<presentation_id>\d+)/slides/(?P<slide_id>\d+)$',
        PresentationSlideView.as_view(), name='presentation_slide'),
    url(r'^presentation/(?P<pk>\d+)/done/$',  # TODO изменить на presentation_id
        PresentationDoneView.as_view(), name='presentationdone'),
]
