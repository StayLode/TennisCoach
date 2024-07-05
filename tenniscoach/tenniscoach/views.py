from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views.static import serve
from . import settings
from django.template.loader import render_to_string
import os

#CBV per renderizzare la pagina di creazione di un Customer
class UserCreateView(CreateView):
    #form_class = UserCreationForm
    form_class = CustomerCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = "Cliente"
        return context
    
#CBV che eredita dalla precedente, per renderizzare la pagina di creazione di un Coach
class CoachCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = CoachCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = "Coach"
        return context

#Vista per autorizzare l'accesso ai media -> video
def authorize_media_resource(request: HttpRequest) -> HttpResponse:
    resource = os.path.basename(request.path)
    if request.user.is_authenticated and request.user.profile.has_permession_auth(resource):
        document_root = settings.MEDIA_ROOT
        media_path = request.path.split("media")[1]
        return serve(request, media_path, document_root, False)
    return redirect("403")

#Vista per renderizzare la pagina 403
def custom_403_view(request):
    return render(request, '403.html', status=403)

#Vista per renderizzare la pagina 404
def custom_404_view(request):
    return render(request, '404.html', status=404)

