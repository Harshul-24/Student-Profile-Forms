from django.contrib.auth import get_user_model
from django.db.models import BooleanField, CASCADE, CharField, EmailField, ForeignKey, Model, OneToOneField, PositiveIntegerField, PositiveSmallIntegerField, PROTECT
from .fields import ImageBinaryField
from django.shortcuts import reverse

class Company(Model):
	name = CharField(max_length = 60)
	logo = ImageBinaryField(default = None, null = True, blank = True, editable = True)
	email = EmailField(null = True, blank = True)
	website = CharField(max_length = 100, null = True, blank = True,)
	telephone = CharField(null = True, blank = True, max_length = 127)
	registered_address = CharField(max_length = 1000, null = True, blank = True, editable = True,)
	employee_expectations = CharField(max_length = 1000, null = True, blank = True, help_text = "Optional\nInclude the company\'s vision, it's expectations from employees at large and relevant info here", editable = True,)
	sector = CharField(max_length = 25, help_text = "e.g., Public, Government, NGO, Startup")
	industry = CharField(max_length = 255, help_text = "Which industry(ies) does the organisation fall in?")
	remarks = CharField(max_length = 255, null = True, blank = True,)

	def get_absolute_url(self):
		return reverse("recruiters:company_detail", kwargs = {"pk" : self.pk})

class Rep(Model):
	userModel = get_user_model()
	user = OneToOneField(userModel, on_delete = CASCADE, related_name = 'Company_Representative', related_query_name = 'rep',)
	company = ForeignKey(Company, on_delete = CASCADE, related_name = 'Company_Representative', related_query_name = 'rep', null = True,)
	contact = CharField(max_length = 15)
	alternate_contact = CharField(max_length = 15)
	alternate_email = EmailField(null = True, blank = True,)
	notes = CharField(null = True, blank = True, help_text = ("Upto 255 characters"), max_length = 255)

class JNF(Model):
	class Meta:
		permissions = [
			('apply_jnf', 'Can apply for the job notified by jnf'),
			('approve_jnf', 'Can approve jnf'),
		]
	company = ForeignKey(Company, on_delete = PROTECT, related_name = 'jnf', related_query_name = 'jnf')
	min_ctc = CharField("Minimum CTC offered (annual)", null = True, blank = True, max_length = 32)
	city = CharField("City(Cities) of Posting", max_length = 40)
	designation = CharField(max_length = 20)
	job_description = CharField(max_length = 1000, null = True, blank = True,)
	skills_required = CharField(max_length = 255, null = True, blank = True,)
	remarks = CharField(max_length = 255, null = True, blank = True,)
	approved = BooleanField(null = False, default = False, blank = True)

	def get_absolute_url(self):
		return reverse("recruiters:jnf_detail", kwargs = {'pk' : self.pk })

