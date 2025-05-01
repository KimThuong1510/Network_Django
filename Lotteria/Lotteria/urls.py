"""
URL configuration for Lotteria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
    path('api/chat/<int:user_id>/', views.api_get_or_create_chat, name='api_get_or_create_chat'),
    path('api/chats/', views.api_get_chats, name='api_get_chats'),
    path('api/messages/<int:chat_id>/', views.api_get_messages, name='api_get_messages'),
    path('api/messages/send/', views.api_send_message, name='api_send_message'),
    path('api/friends/request/', views.api_send_friend_request, name='api_send_friend_request'),
]
