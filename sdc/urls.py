"""sdc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accountviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls', namespace = 'profiles')),
    path("recruiters/", include("recruiters.urls", namespace = "recruiters")),
    path('accounts/', include('accounts.urls', namespace = 'accounts')),
    path('icdpc/', include('icdpc.urls', namespace = 'icdpc')),
	path('reset/<uidb64>/<token>', accountviews.CustomPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
	path('password_reset_done', accountviews.CustomPasswordResetDoneView.as_view(), name = 'password_reset_done'),
	path('reset/done', accountviews.CustomPasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
]