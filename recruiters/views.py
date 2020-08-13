import csv
from accounts.models import has_perm, assign_perm, get_object
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, reverse, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import DetailView, TemplateView
from django.views.generic.list import ListView
from .forms import JNFModelForm, CompanyModelForm, RepModelForm
from .models import Company, JNF, Rep
from .widgets import CustomComboWidget
from functools import wraps

fp = open("world-cities_unicode.csv", "rt", newline = "", encoding = "UTF-8-sig")
data = csv.reader(fp)
country_list = []
for row in data:
	if (row[1],row[1]) not in country_list:
		country_list.append((row[1], row[1]))
country_list.sort()

def get_cities_response(request):
	country = request.GET.get("country")
	data = { "data" : get_cities(country = country) }
	return JsonResponse(data)

def registration_permission_check(argument_list):
	def decorator(func):
		@login_required
		@wraps(func)
		def inner_func(request, *args, **kwargs):
			try:
				request.rep = Rep.objects.get(user = request.user)
			except (Rep.DoesNotExist, TypeError):
				return redirect(reverse("recruiters:rep_create"))
			try:
				if not hasattr(request, 'rep') or request.rep is None:
					request.company = get_object(request.user, "recruiters.view_company", Company)
				else:
					request.company = Company.objects.get(rep__user = request.user)
			except (Company.DoesNotExist, TypeError):
				return redirect(reverse("recruiters:company_create"))
			# check for object specific permissions
			if len(argument_list) != 0:
				if not has_perm(request.user, argument_list[0], kwargs['pk']):
					# check for universal permissions
					if not request.user.has_perm(argument_list[0]):
						raise PermissionDenied
			return_value = func(request, *args, **kwargs)
			return return_value
		return inner_func
	return decorator

@method_decorator(login_required, name = "dispatch")
class CompanyCreateView(CreateView):
	model = Company
	form_class = CompanyModelForm
	success_url = '/recruiters/home'
	def setup(self, request, *args, **kwargs):
		super(CompanyCreateView, self).setup(request, *args, **kwargs)
		try:
			self.request.rep = Rep.objects.get(user = request.user)
		except Rep.DoesNotExist or TypeError:
			self.request.rep = None
	def form_valid(self, form):
		with transaction.atomic():
			comp = Company.objects.create(**form.cleaned_data)
			self.request.company = comp
			# Assign the company to rep
			# Please note that self.request.rep is a Python object 
			# created from the values available in the database at the time of creation
			# Updating the company attribute on self.request.rep will not change 
			# the value in the database unless you call save() on it
			if self.request.rep is not None:
				Rep.objects.filter(pk = self.request.rep.pk).update(company = self.request.company)
			assign_perm(self.request.user, "recruiters.change_company", comp.pk)
			assign_perm(self.request.user, "recruiters.delete_company", comp.pk)
			assign_perm(self.request.user, "recruiters.view_company", comp.pk)
		return redirect(self.success_url)

@method_decorator(registration_permission_check(["recruiters.view_company"]), name = 'dispatch' )
class CompanyDetailView(DetailView):
	model = Company

@method_decorator(registration_permission_check(["recruiters.view_company"]), name = 'dispatch' )
class CompanyListView(ListView):
	def get_queryset(self):
		return get_object_list(self.request.user, "recruiters.view_company", Company)

@method_decorator(registration_permission_check(["recruiters.change_company"]), name = 'dispatch' )
class CompanyUpdateView(UpdateView):
	model = Company
	form_class = CompanyModelForm

@method_decorator(registration_permission_check([]), name = 'dispatch' )
class HomeView(ListView):
	template_name = 'recruiters/home.html'
	http_method_names = ["get",]
	def get_queryset(self):
		return JNF.objects.filter(company = self.request.company)

@method_decorator(registration_permission_check([]), name = 'dispatch' )
class JNFCreateView(CreateView):
	model = JNF
	form_class = JNFModelForm
	http_method_names = ["get", "post"]
	success_url = '/recruiters/home'
	def form_valid(self, form):
		print(self.request.POST)
		with transaction.atomic():
			jnf = JNF.objects.create(company = self.request.company, **form.cleaned_data )
			assign_perm(self.request.user, "recruiters.change_jnf", jnf.pk)
			assign_perm(self.request.user, "recruiters.view_jnf", jnf.pk)
			assign_perm(self.request.user, "recruiters.delete_jnf", jnf.pk)
		return redirect(self.success_url)

@method_decorator(registration_permission_check(["recruiters.view_jnf"]), name = 'dispatch' )
class JNFDetailView(DetailView):
	http_method_names = ["get"]
	model = JNF

class JNFListView(ListView):
	def get_queryset(self):
		return get_object_list(self.request.user, "recruiters.view_jnf", JNF)

@method_decorator(registration_permission_check(["recruiters.change_jnf"]), name = 'dispatch' )
class JNFUpdateView(UpdateView):
	http_method_names = ["get", "post"]
	form_class = JNFModelForm
	success_url = '/recruiters/home'

@method_decorator(login_required, name = "dispatch")
class RepCreateView(CreateView):
	def setup(self, request, *args, **kwargs):
		super(RepCreateView, self).setup(request, *args, **kwargs)
		try:
			self.request.rep = Rep.objects.get(user = request.user)
		except Rep.DoesNotExist or TypeError:
			self.request.rep = None
	model = Rep
	http_method_names = ["get", "post"]
	form_class = RepModelForm
	success_url = '/recruiters/home'
	def form_valid(self, form):
		if not hasattr(self.request, 'company') or self.request.company is None:
			with transaction.atomic():
				rep = Rep.objects.create(user = self.request.user, **form.cleaned_data)
				self.request.rep = rep
				assign_perm(self.request.user, "recruiters.change_rep", rep.pk)
				assign_perm(self.request.user, "recruiters.delete_rep", rep.pk)
				assign_perm(self.request.user, "recruiters.view_rep", rep.pk)
		else:
			with transaction.atomic():
				rep = Rep.objects.create(user = self.request.user, company = self.request.company, **form.cleaned_data)
				self.request.rep = rep
				assign_perm(self.request.user, "recruiters.change_rep", rep.pk)
				assign_perm(self.request.user, "recruiters.delete_rep", rep.pk)
				assign_perm(self.request.user, "recruiters.view_rep", rep.pk)
		return redirect(self.success_url)

@method_decorator(registration_permission_check(["recruiters.view_rep"]), name = 'dispatch' )
class RepDetailView(DetailView):
	http_method_names = ["get",]
	model = Rep

@method_decorator(registration_permission_check(["recruiters.change_rep"]), name = 'dispatch' )
class RepUpdateView(UpdateView):
	success_url = "/recruiters/home"
	http_method_names = ["get", "post"]
	form_class = RepModelForm
	model = Rep
	def form_valid(self, form):
		Rep.objects.filter(pk = self.object.pk).update(**form.cleaned_data)
		return redirect(self.success_url)