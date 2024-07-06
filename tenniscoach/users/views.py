from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic.detail import DetailView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.paginator import Paginator

from essential.models import *
# Create your views here.

#CBV che mostra il profilo dell'utente loggato
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        # Ottieni l'ID utente dall'URL
        
        profile_id = int(self.kwargs['pk'])

        #Verifica che tale profilo esista, altrimenti 404
        try:
            _ = get_object_or_404(Profile, pk=profile_id)
        except Http404:
            return redirect("404")

        # Verifica se l'ID utente corrisponde a quello dell'utente loggato
        if profile_id != self.request.user.id and not self.request.user.is_staff:
            # Se non corrisponde, restituisci una risposta 403
            return redirect("403")
        return super().dispatch(request, *args, **kwargs)

#FBV che permette di aggiornare il proprio profilo
@login_required
def modify_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Salvataggio dei dati nel database
            
            messages.success(request, "Profilo modificato con successo!")
            form.save()
            return redirect('users:profile', profile.pk)  # Reindirizza a una vista successiva
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})

#CBV che mostra una pagina profilo di un coach con i relativi corsi messi a disposizione
class CoachProfileDetailView(DetailView):
    model = Profile
    template_name = "presentation.html"
    
    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            coach_group = Group.objects.get(name='Coach')
            
            # Verifica se l'utente associato al profilo è un coach
            if not (self.object.user.groups.filter(name=coach_group.name).exists() or self.object.user.is_staff):
                return redirect("403")
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return redirect("404")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        order_by = self.request.GET.get('order_by', '')
        
        courses = Course.objects.filter(user_id = self.object.id)
        try:
            if order_by:
                courses = courses.order_by(order_by)
            else:
                courses = courses.order_by("-purchases_number")
        except:
            pass

        paginator = Paginator(courses, 6)  # 6 corsi per pagina
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['full_name'] = f"{self.object.name} {self.object.surname}" if self.object.name and self.object.surname else None
        return context
    
#CBV che permette di visualizzare l'elenco dei corsi acquistati dall'utente
class YourCoursesListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "dashboard.html"
    
    paginate_by = 6

    def get_queryset(self):
        queryset =  self.request.user.profile.purchases.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by("-purchase__date")
        
        return queryset

#CBV che gestisce il cambiamento della password per l'utente loggato
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_message = "Password modificata con successo!"

    def form_valid(self, form):
        # Aggiungi il messaggio di successo
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_success_url(self):
        # Costruisci l'URL di successo con l'ID dell'utente
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})