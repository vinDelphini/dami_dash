"""dami URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from allauth.account.views import LoginView
from app.views import HomeRedirect
from common.forms import AxesLoginForm
from axes.decorators import axes_dispatch, axes_form_invalid

urlpatterns = [
    path("", HomeRedirect.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path(
        "accounts/login/",
        LoginView.as_view(form_class=AxesLoginForm),
        name="account_login",
    ),
    path("accounts/", include("allauth.urls")),
    path("invitations/", include("invitations.urls", namespace="invitations")),
]
