from django.shortcuts import render, redirect
from .models import *
from django.views.generic.detail import DetailView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Group

from django.core.paginator import Paginator

from essential.models import *
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


class CoachProfileDetailView(DetailView):
    model = Profile
    template_name = "presentation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verifica se l'utente associato al profilo è un coach
        coach_group = Group.objects.get(name='Coach')
        if not (self.object.user.groups.filter(name=coach_group.name).exists() or self.object.user.is_superuser):
            raise PermissionDenied

        order_by = self.request.GET.get('order_by', 'title')
        
        courses = Course.objects.filter(user_id = self.object.id)
        if order_by:
            courses = courses.order_by(order_by)
        
        paginator = Paginator(courses, 6)  # 6 corsi per pagina
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context['page_obj'] = page_obj
        context['order_by'] = order_by
        context['full_name'] = f"{self.object.name} {self.object.surname}" if self.object.name and self.object.surname else None
        context['courses'] = courses
        return context
    

    
class YourCoursesListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "dashboard.html"
    
    paginate_by = 6

    def get_queryset(self):
        queryset =  self.request.user.profile.purchases.all()
        order_by = self.request.GET.get('order_by', 'title')
        if order_by:
           queryset = queryset.order_by(order_by)
        
        return queryset