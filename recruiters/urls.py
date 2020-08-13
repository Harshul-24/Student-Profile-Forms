from django.urls import path
from . import views

app_name = "recruiters"
urlpatterns = [
	path('home', views.HomeView.as_view(), name = "home"),
	path('company_update/<int:pk>', views.CompanyUpdateView.as_view(), name = "company_update"),
	path('company_register', views.CompanyCreateView.as_view(), name = "company_create"),
	path('view_company/<int:pk>', views.CompanyDetailView.as_view(), name = "company_detail"),
	path('jnf_create', views.JNFCreateView.as_view(), name = "jnf_create"),
	path('jnf_update/<int:pk>', views.JNFUpdateView.as_view(), name = "jnf_update"),
	path("view_jnf/<int:pk>", views.JNFDetailView.as_view(), name = "jnf_detail"),
	path('register', views.RepCreateView.as_view(), name = 'rep_create'),
	path('update/<int:pk>', views.RepUpdateView.as_view(), name = "rep_update"),
	path('detail/<int:pk>', views.RepDetailView.as_view(), name = "rep_detail"),
]	