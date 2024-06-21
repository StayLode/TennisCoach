from django.urls import path, re_path
from .views import *

app_name = "essential"

urlpatterns = [
	re_path(r"^$|^\/$|^home\/$", tennis_home, name="home"),
	path("courses/", CoursesListView.as_view(), name="listacorsi"),
    path("course/<pk>/", CorsoDetailView.as_view(), name="corso"),
    path('your_courses/', YourCoursesListView.as_view(), name='dashboard'),
    
    path('save_course/<int:course_id>/', save_course, name='save_course'),

] 
