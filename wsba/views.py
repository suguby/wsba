#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import request, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView

from presentations.models import Organisation
from wsba.forms import PrefaceForm


class IndexView(TemplateView):
    template_name = 'index.html'


class PrefaceView(FormView):
    template_name = 'preface.html'

    def get(self, request):
        form = PrefaceForm()
        return render(request, 'preface.html', {'form': form})

    def post(self, request, *args, **kwargs):

        if Organisation.objects.filter(name=request.POST.get('Organisation_name')):
            # пометить поле как невалидное и сообщить, что такая организация уже есть
            form = PrefaceForm()
            form.errors['Organisation_name'] = ["Организация уже зарегистрирована ранее"]
            return self.form_invalid(form)
        else:
            new_org = Organisation(name=request.POST.get('Organisation_name'))
            new_org.save()
        return HttpResponseRedirect('/thanks/')

class ThanksView(TemplateView):
    template_name = 'thanks.html'