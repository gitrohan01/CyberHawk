"""
URL configuration for cyberhawk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from core import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    # Custom admin login page
    path('admin-login/', views.custom_admin_login, name='custom_admin_login'),
    # Home / New Scan
    path('', views.home, name='home'),

    # Main scan results (specific scan by ID)
    path('scan/<int:scan_id>/', views.results, name='results'),

    # Individual results pages
    path('info-results/', views.info_results, name='info_results'),
    path('enumeration-results/', views.enumeration_results, name='enumeration_results'),
    path('service-results/', views.service_results, name='service_results'),
    path('web-results/', views.web_results, name='web_results'),
    path('report/', views.report, name='report'),
]


