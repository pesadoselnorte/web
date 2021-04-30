"""app URL Configuration

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

from extras.views import ExtrasView
from django.conf import settings
from django.conf.urls.static import static
#from django.views.generic.base import TemplateView

admin.site.site_header = "Pesados El Norte"
admin.site.site_title = "Pesados El Norte"
admin.site.index_title = "Panel de control"

urlpatterns = [
    path('', ExtrasView.as_view(), name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('extras/', ExtrasView.as_view(), name='home'),
]

from django.contrib.auth.models import User, Group

admin.site.unregister(Group)
if not User.is_superuser:
    admin.site.unregister(User)
