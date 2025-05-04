"""
URL configuration for Lotteria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import home
    2. Add a URL to urlpatterns:  path('', home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mxh import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('user_home/', views.user_home, name='user_home'),
    path('task/', views.task_view, name='task_view'),
    path('chat/', views.chat_view, name='chat_view'),
    path('nofication_company/', views.company_view, name='company_view'),
    path('create_post/', views.create_post, name='create_post'),
    path('user_home/', views.post_detail, name='post_detail'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('search/', views.search_employees, name='search_employees'),
    path('chat/<int:chat_id>/', views.chat_room, name='chat_room'),
    path('chat/<int:chat_id>/send/', views.add_message, name='add_message'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_chat_room, name='group_chat_room'),
    path('group/<int:group_id>/add_message/', views.add_group_message, name='add_group_message'),

]

