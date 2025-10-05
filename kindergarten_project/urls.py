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
from kindergarten_app_.views import register_user, user_login, add_employee, get_educational_program_by_id, \
    add_parent, list_parents, list_employees, get_parent_by_user_id, create_group, edit_parent, add_child, \
    get_employee_by_user_id, create_educational_program, list_groups, get_group_by_id, edit_group, edit_employee, \
    get_child, edit_child, assign_employee_role, add_event, events_by_educational_program, get_event, edit_event


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user, name='register'),
    path('api/login/', user_login, name='login'),
    path('api/employee/add/', add_employee, name='add_employee'),
    path('api/parent/add/', add_parent, name='add_parent'),
    path('api/parent/list/', list_parents, name='list_parents'),
    path('api/parent/edit/<int:parent_id>/', edit_parent, name='edit_parent'),
    path('api/employee/list/', list_employees, name='list_employees'),
    path('api/employee/list/<int:user_id>/', get_employee_by_user_id, name='get_employee_by_user_id'),
    path('api/employee/edit/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('api/parent/list/<int:user_id>/', get_parent_by_user_id, name='get_parent_by_user_id'),
    path('api/education_program/create/', create_educational_program, name='create_educational_program'),
    path('api/education_program/<int:program_id>/', get_educational_program_by_id, name='get_education_program_by_id'),
    path('api/group/create/', create_group, name='create_group'),
    path('api/group/list/', list_groups, name='list_groups'),
    path('api/group/<int:group_id>/', get_group_by_id, name='get_group_by_id'),
    path('api/group/edit/<int:group_id>/', edit_group, name='edit_group'),
    path('api/child/add/', add_child, name='add_child'),
    path('api/child/<int:child_id>/', get_child, name='get_child'),
    path('api/child/edit/<int:child_id>/', edit_child, name='edit_child'),
    path('api/group/role/', assign_employee_role, name='assign_employee_role'),
    path('api/event/add/', add_event, name='create_event'),
    path('api/events/educational_program/<int:educational_program_id>/', events_by_educational_program, name='events_by_educational_program'),
    path('api/event/<int:event_id>/', get_event, name='view_event_by_id_for_parent'),
    path('api/event/edit/<int:event_id>/', edit_event, name='edit_event'),

]
