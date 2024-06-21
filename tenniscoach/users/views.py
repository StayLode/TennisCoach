from django.shortcuts import render, redirect
from .models import *
from django.views.generic.detail import DetailView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile.html"

@login_required
def modifica_profilo(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Salvataggio dei dati nel database
            form.save()
            return redirect('users:profile', profile.pk)  # Reindirizza a una vista successiva
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})

