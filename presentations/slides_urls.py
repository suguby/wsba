from django.conf.urls import url
from django.views.generic import TemplateView

from presentations.views import SlideView

urlpatterns = [
    url(r'(?P<slide>[0-9]+)$', SlideView.as_view(), name='slide_view'),
    url(r'test1/$', TemplateView.as_view(template_name='presentations/test.html'))
]
