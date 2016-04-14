from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView

from user_interface.models import ProjectUser


class RegistrationView(TemplateView):
    template_name = 'registration/index.html'

    def get_context_data(self, **kwargs):
        form = UserCreationForm()
        context = dict(form=form)
        return context

    def post(self, request, **kwargs):
        form = UserCreationForm(data=self.request.POST)
        if form.is_valid():
            ProjectUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            return HttpResponseRedirect(redirect_to=form.cleaned_data['next'])
        context = dict(form=form)
        return self.render_to_response(context=context)
