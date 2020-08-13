from .models import Company, JNF, Rep
from django.forms import ModelForm

class CompanyModelForm(ModelForm):
	class Meta:
		model = Company
		exclude = ("approved",)

class JNFModelForm(ModelForm):
	class Meta:
		model = JNF
		exclude = ("company", "approved",)

class RepModelForm(ModelForm):
	class Meta:
		model = Rep
		exclude = ("company", "user",)