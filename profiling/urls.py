from django.urls import path
from . import views

app_name = 'profiling'

urlpatterns = [
    # /music/
    path('', views.IndexView.as_view(), name='index'),
    path('<pk>', views.DetailView.as_view(), name='detail'),
    path('student/add', views.StudentCreate.as_view(), name='student-add'),

    ]