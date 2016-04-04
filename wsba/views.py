#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import request
from django.shortcuts import redirect
from django.views.generic import TemplateView

from presentations.models import Organisation


class IndexView(TemplateView):
    template_name = 'index.html'

class PrefaceView(TemplateView):
    template_name = 'preface.html'

    def post(self, request, *args, **kwargs):
        if Organisation.objects.filter(name=request.POST.get('Organisation_name')):
            # пометить поле как невалидное и сообщить, что такая организация уже есть
            pass
        else:
            new_org = Organisation(name=request.POST.get('Organisation_name'))
            new_org.save()
        return redirect(reverse('preface', kwargs=kwargs))