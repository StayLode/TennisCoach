from typing import Any
from django.http.response import HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpRequest, HttpResponse

# pipenv install django-braces
from braces.views import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.db.models import Q
from functools import reduce
import operator
from .models import *
from .forms import *
from users.models import Profile


def tennis_home(request):
    return render(request, template_name="home.html")

class CoursesListView(ListView):
    title = "Corsi disponibili"
    model = Course
    template_name = "courses_list.html"
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
            if user.groups.filter(name="Coach").exists():
                context["coaches"].add(user)
        
        context["ordinamenti"]=["Titolo", "Prezzo", "Data"]
        context["livelli"] = ["Principiante", "Intermedio", "Esperto"]
        return context


class CorsoDetailView(DetailView):
    model = Course
    template_name = "course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = Lesson.objects.filter(course__pk=context["object"].pk)
        for coach in Profile.objects.all():
            if coach.pk == context["object"].user.pk:
                context["coach"] = coach

        user = self.request.user

        purchased=Purchase.objects.filter(course_id=context["object"].pk)
        context["saved_by_current_user"] = purchased.filter(user_id=user.id).exists()
        if self.object.user_id == user.id:
            context["is_the_creator"] = True
        else:
            context["is_the_creator"] = False
        return context

@login_required
def save_course(request, course_id):
    corso = get_object_or_404(Course, id=course_id)
    utente = request.user
    if (utente.id == corso.user_id):
        message = "Il corso è di tua proprietà!"
        messages.warning(request, message)
        return redirect("essential:createdcourses")
    # Verifica se l'utente ha già salvato questo corso
    _, created = Purchase.objects.get_or_create(user=utente.profile, course=corso, defaults={'date': timezone.now()})

    if created:
        message = "Corso salvato con successo!"
        messages.success(request, message)
    else:
        message = "Hai già salvato questo corso."
        messages.warning(request, message)
    
    
    return redirect("users:dashboard")



#Views solo per i coach

class GroupRequiredMixin(AccessMixin):
    group_required = None
    def test_func(self):
        if "lesson" in self.request.path and "create_lesson" not in self.request.path :
            lesson_id = self.kwargs.get('pk')
            lesson = get_object_or_404(Lesson, id=lesson_id)
            return (lesson.course.user_id == self.request.user.id) or self.request.user.is_staff
        else:
            id = self.kwargs.get('course_id')
            if not id:
                id = self.kwargs.get('pk')
            if not id:
                return True
            course = get_object_or_404(Course, id=id)
            return (course.user_id == self.request.user.id) or self.request.user.is_staff

           
    
    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        
        user_groups = request.user.groups.values_list('name', flat=True)
        if (not set(self.group_required).intersection(set(user_groups))) and not self.request.user.is_staff:
            print("QUA")
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect('403')

class CreatedCoursesListView(GroupRequiredMixin, ListView):
    group_required = ["Coach"]
    template_name = "manage_courses.html"
    model = Course
    paginate_by = 9
    

    def get_queryset(self):
        queryset = super().get_queryset().filter(user_id = self.request.user.pk)
        order_by = self.request.GET.get('order_by', 'title')
        if order_by:
           queryset = queryset.order_by(order_by)
        
        return queryset

class CreateCourseView(GroupRequiredMixin, CreateView):
    group_required = ["Coach"]
    form_class = CreateCorsoForm
    template_name = "create.html"
    success_url = reverse_lazy("essential:createdcourses")
    
    success_message = "Corso creato con successo!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = "corso"
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user.profile  # Associa l'utente corrente come creatore del corso
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class CreateLessonView(CreateCourseView):
    form_class = CreateLessonForm
    success_message = "Lezione aggiunta con successo!"

    def get_success_url(self) -> str:
        return reverse_lazy("essential:corso", kwargs={'pk': self.object.course.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        context['tipo'] = "lezione"
        return context
    
    def form_valid(self, form):
        # Ottieni il course_id dalla richiesta
        course_id = self.kwargs.get('course_id')
        # Assegna il course_id al form prima di salvarlo

        course = get_object_or_404(Course, pk=course_id)
        if course.user_id != self.request.user.id:
            return redirect("404")
        

        form.instance.course_id = course_id

        return super().form_valid(form)    
    
        
class DeleteCourseView(GroupRequiredMixin, DeleteView):
    group_required = ["Coach"]
    template_name = "delete.html"
    model = Course
    success_message = "Corso eliminato con successo!"
    success_url = reverse_lazy("essential:createdcourses")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entita"] = "Corso"
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        obj.delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

class DeleteLessonView(DeleteCourseView):
    model = Lesson
    success_message = "Lezione eliminata con successo!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entita"] = "Lezione"
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        course_pk = obj.course.pk
        obj.delete()
        messages.success(self.request, self.success_message)
        # Chiamare self.get_success_url() per ottenere l'URL di successo
        return redirect(reverse_lazy("essential:corso", kwargs={"pk": course_pk}))

class UpdateCorsoView(GroupRequiredMixin, UpdateView):
    group_required = ["Coach"]
    model = Course
    template_name = "edit.html"
    form_class = CreateCorsoForm

    def get_success_url(self):
        return reverse_lazy("essential:corso", kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["entita"] = "Corso"
        return context
    
class UpdateLessonView(UpdateCorsoView):
    model = Lesson
    form_class = CreateLessonForm

    def get_success_url(self):
        return reverse_lazy("essential:corso", kwargs={'pk': self.object.course.pk})
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["entita"] = "Lezione"
        return context
    

