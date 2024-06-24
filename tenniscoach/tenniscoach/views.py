from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.static import serve
from . import settings
from django.template.loader import render_to_string
import os

def tennis_home(request):
    return render(request, template_name="home.html")

class UserCreateView(CreateView):
    #form_class = UserCreationForm
    form_class = CustomerCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = "Cliente"
        return context

class CoachCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = CoachCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = "Coach"
        return context


def authorize_media_resource(request: HttpRequest) -> HttpResponse:
    resource = os.path.basename(request.path)
    if request.user.is_authenticated and request.user.profile.has_permession_auth(resource):
        document_root = settings.MEDIA_ROOT
        media_path = request.path.split("media")[1]
        return serve(request, media_path, document_root, False)
    html = render_to_string('404.html', {})
    return HttpResponseNotFound(html)

    

def custom_404_view(request):
    return render(request, '404.html', status=404)

