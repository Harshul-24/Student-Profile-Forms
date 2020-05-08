from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Student

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'profiling/index.html'
    context_object_name = 'all_students'

    def get_queryset(self):
        return Student.objects.all()

class DetailView(generic.DetailView):
    model = Student
    template_name = 'profiling/detail.html'


class StudentCreate(CreateView):
    model = Student
    fields =['name', 'roll_number', 'department' ]

