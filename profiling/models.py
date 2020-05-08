from django.db import models
from django.urls import reverse
BIO = "Biological Sciences"
CHM = "Chemistry"
CHE = "Chemical Engineering"
ECS = "Electrical engg. & Computer Science"
EES = "Earth and Environment Science"
MTH = "Mathematics"
PHY = "Physics"

DEPARTMENT_CHOICES = (
      ( BIO,"Biological Sciences"),
      ( CHM,"Chemistry"),
      ( CHE, "Chemical Engineering"),
      ( ECS, "Electrical engg. & Computer Science"),
      ( EES, "Earth and Environment Science"),
      ( MTH, "Mathematics"),
      ( PHY, "Physics")

)

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.PositiveIntegerField(primary_key=True)
    department =  models.CharField(
        max_length = 100,
        choices = DEPARTMENT_CHOICES,
        default = BIO,
    )

    def get_absolute_url(self):
        return reverse('profiling:detail', kwargs={'pk': self.pk})

    def __str__(Student):
        return Student.name + "--> " + str(Student.roll_number)

class Profile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    internship = models.TextField(max_length=500)
    experience = models.TextField(max_length=500)
    non_scholastic = models.TextField(max_length=200, blank=True)





