from django.conf.urls import url
from django.views.generic import TemplateView

from presentations.views import SlideView

urlpatterns = [
    url(r'(?P<slide_id>[0-9]+)$', SlideView.as_view(), name='slide_view'),

]
