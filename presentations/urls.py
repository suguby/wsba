from django.conf.urls import url

from presentations.views import SlideView

urlpatterns = [
    url(r'organisation/([0-9]+)/presentation/([0-9]+)/slide/([0-9]+)', SlideView.as_view(), name='slide_view'),
]
