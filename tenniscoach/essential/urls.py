from django.urls import path, re_path
from .views import *

app_name = "essential"

urlpatterns = [

    # Home 
	re_path(r"^$|^\/$|^home\/$", tennis_home, name="home"),

    # Lista dei corsi
	path("courses/", CoursesListView.as_view(), name="courseslist"),

    # Dettagli di un corso
    path("course/<int:pk>/", CourseDetailView.as_view(), name="corso"),

    # Salvataggio di un corso
    path('save_course/<int:course_id>/', save_course, name='save_course'),
    
    # Corsi creati da un coach
    path('created_courses/', CreatedCoursesListView.as_view(), name = "createdcourses"),

    # Operazioni Create - Update - Delete su corsi e lezioni 
    path('create_lesson/<int:course_id>/', CreateLessonView.as_view(), name="createlesson"),
    path('create/', CreateCourseView.as_view(), name="createcorso"),

    path('edit_lesson/<int:pk>/', UpdateLessonView.as_view(), name="editlesson"),
    path('edit/<int:pk>/', UpdateCourseView.as_view(), name="editcorso"),

    path('delete_lesson/<int:pk>/', DeleteLessonView.as_view(), name="deletelesson"),
    path('delete/<int:pk>/', DeleteCourseView.as_view(), name="deletecorso"),

    # Endpoint per lista dei coach
    path('ajax/search/coaches/', ajax_search_coaches, name='ajax_search_coaches'),

] 
