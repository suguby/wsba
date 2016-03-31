from django.conf.urls import url
from django.views.generic import TemplateView

from presentations.views import SlideView

urlpatterns = [
    url(r'organization/([0-9]+)/presentation/([0-9]+)/slide/([0-9]+)$', SlideView.as_view(), name='slide_view'),
]
