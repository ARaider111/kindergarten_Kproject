"""
URL configuration for kindergarten_project project.

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
from django.contrib import admin
from django.urls import path
from kindergarten_app_.views import register_user, user_login, add_employee, \
    add_parent, list_parents, list_employees, get_parent_by_user_id, get_employee_by_user_id


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user, name='register'),
    path('api/login/', user_login, name='login'),
    path('api/employee/add/', add_employee, name='add_employee'),
    path('api/parent/add/', add_parent, name='add_parent'),
    path('api/parent/list/', list_parents, name='list_parents'),
    path('api/employee/list/', list_employees, name='list_employees'),
    path('api/parent/list/<int:user_id>/', get_parent_by_user_id, name='get_parent_by_user_id'),
    path('api/employee/list/<int:user_id>/', get_employee_by_user_id, name='get_employee_by_user_id'),
]
