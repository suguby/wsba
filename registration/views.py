from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from user_interface.models import ProjectUser


class RegistrationView(TemplateView):
    template_name = 'registration/index.html'

    def get_context_data(self, **kwargs):
        form = UserCreationForm()
        context = dict(
            form=form,
            next=self.request.GET.get('next', '/'),
        )
        return context

    def post(self, request, **kwargs):
        form = UserCreationForm(data=self.request.POST)
        if form.is_valid():

            ProjectUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            return HttpResponseRedirect(redirect_to=self.request.GET.get('next', '/'))
        context = dict(form=form)
        return self.render_to_response(context=context)
