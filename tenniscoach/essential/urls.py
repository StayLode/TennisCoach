from django.urls import path, re_path
from .views import *

app_name = "essential"

urlpatterns = [
	re_path(r"^$|^\/$|^home\/$", tennis_home, name="home"),
	path("courses/", CoursesListView.as_view(), name="listacorsi"),
    path("course/<int:pk>/", CorsoDetailView.as_view(), name="corso"),
    path('save_course/<int:course_id>/', save_course, name='save_course'),
    
    path('created_courses/', CreatedCoursesListView.as_view(), name = "createdcourses"),

    path('create_lesson/<int:course_id>/', CreateLessonView.as_view(), name="createlesson"),
    path('create/', CreateCourseView.as_view(), name="createcorso"),

    path('edit_lesson/<int:pk>/', UpdateLessonView.as_view(), name="editlesson"),
    path('edit/<int:pk>/', UpdateCorsoView.as_view(), name="editcorso"),

    path('delete_lesson/<int:pk>/', DeleteLessonView.as_view(), name="deletelesson"),
    path('delete/<int:pk>/', DeleteCourseView.as_view(), name="deletecorso"),
] 
