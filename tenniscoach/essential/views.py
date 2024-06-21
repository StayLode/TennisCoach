from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from django.db.models import Q
from functools import reduce
import operator
from .models import *
from users.models import Profile


def tennis_home(request):
    return render(request, template_name="home.html")

class CoursesListView(ListView):
    title = "Corsi disponibili"
    model = Course
    template_name = "lista_corsi.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('query', '')

        # Trying to imitate full text search.
        splitted_query = query.split()
        conditions_gen = (Q(title__icontains=word) for word in splitted_query)
        ft_query = reduce(operator.and_, conditions_gen, Q())

        queryset = queryset.filter(ft_query)
        coach = self.request.GET.get('coach', '')
        level = self.request.GET.get('level','')
        ordering = self.request.GET.get('ordering','')
        order_by = self.request.GET.get('order_by','')
        paid = self.request.GET.get('paid', '')
        free = self.request.GET.get('free','')
        
        choices = {
            "Prezzo":"price",
            "Data": "date",
            "Titolo": "title"
        }

        try:
            if bool(paid) and not bool(free):
                queryset = queryset.filter(price__gt=0)
                
            elif bool(free) and not bool(paid):
                queryset = queryset.filter(price=0) 
        except:
            pass
        
        try:
            queryset = queryset.filter(user__username__icontains=coach)
        except:
            pass

        try:
            queryset = queryset.filter(category__icontains=level)
        except:
            pass
        try:
            if order_by:
                queryset = queryset.order_by(ordering+choices[order_by])
        except:
            pass

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["coaches"]=set()
        for user in User.objects.all():
            if user.is_staff:
                context["coaches"].add(user)
        
        context["ordinamenti"]=["Titolo", "Prezzo", "Data"]
        context["livelli"] = ["Principiante", "Intermedio", "Esperto"]
        return context


class CorsoDetailView(DetailView):
    model = Course
    template_name = "corso.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"]= Lesson.objects.filter(course__pk=context["object"].pk)
        for coach in Profile.objects.all():
            if coach.pk==context["object"].user.profile.pk:
                context["coach"]=coach

        user = self.request.user

        purchased=Purchase.objects.filter(corso_id=context["object"].pk)
        context["saved_by_current_user"]= purchased.filter(utente_id=user.id).exists()
        return context


class YourCoursesListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "dashboard.html"
    
    paginate_by = 9

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.filter(utente_id = self.request.user.id)
        return queryset.order_by("-date")


@login_required
def save_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    # Verifica se l'utente ha già salvato questo corso
    purchase, created = Purchase.objects.get_or_create(utente=user, corso=course, defaults={'date': timezone.now()})

    if created:
        message = "Corso salvato con successo!"
    else:
        message = "Hai già salvato questo corso."
    
    messages.success(request, message)
    return redirect("essential:dashboard")
