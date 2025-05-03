from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Comment, PrivateChat, PrivateMessage, Friend, GroupChat, GroupMember
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, F, OuterRef, Subquery
from django.utils import timezone
import json
import logging

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user_home')
    return render(request, 'mxh/login/login.html')

@login_required
def admin_home(request):
    return render(request, 'mxh/chat/chat_admin.html')

@login_required
def user_home(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('user_home')
    else:
        form = PostForm()

    comments = Comment.objects.all()  # Lấy tất cả bình luận
    posts = Post.objects.all().order_by('-created_at')  # Lấy tất cả bài viết
    chat = PrivateChat.objects.filter(Q(user1=request.user) | Q(user2=request.user)).first()
    context = {
        'form': form,
        'posts': posts,
        'comments': comments,
        'default_chat_id': chat.id if chat else None,  # thêm dòng này
    }
    return render(request, 'mxh/home/home.html', context)

@login_required
def task_view(request):
    return render(request, 'mxh/task/task.html')

@login_required
def chat_view(request):
    return render(request, 'mxh/chat/chat.html')

@login_required
def company_view(request):
    return render(request, 'mxh/nofication/Company.html')

# Tạo bài viết
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('user_home')
    else:
        form = PostForm()
    return render(request, 'mxh/home/create_post.html', {'form': form})

# Bình luận
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)
        Comment.objects.create(post=post, user=request.user, content=content)

    return redirect('user_home')

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'mxh/home/home.html', context)

# Tìm kiếm tên và bộ phận
User = get_user_model()
def search_employees(request):
    query = request.GET.get('q', '')
    department_id = request.GET.get('department', '')
    users = User.objects.all()

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    if department_id:
        users = users.filter(department_id=department_id)

    from .models import Department
    departments = Department.objects.all()

    context = {
        'users': users,
        'query': query,
        'department_id': department_id,
        'departments': departments,
    }
    return render(request, 'mxh/home/home.html', context)

# chat tin nhắn cá nhân

def add_message(request, chat_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        chat = get_object_or_404(PrivateChat, id=chat_id)
        PrivateMessage.objects.create(chat=chat, sender=request.user, content=content)
    return redirect('chat_room', chat_id=chat_id)


def chat_room(request, chat_id):
    chat = get_object_or_404(PrivateChat,  id=chat_id)
    messages = chat.privatemessage_set.all().order_by('sent_at')
    other_user = chat.get_receiver(request.user)

    context = {
        'chat': chat,
        'messages': messages,
        'other_user': other_user,
    }
    return render(request, 'mxh/chat/chat.html', context)

# Tạo nhóm chat
@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        member_ids = request.POST.getlist('members')

        group = GroupChat.objects.create(group_name=group_name, created_by=request.user)

        # Thêm người tạo nhóm
        GroupMember.objects.create(group=group, user=request.user, role='admin')

        # Thêm các thành viên được chọn
        for member_id in member_ids:
            user = User.objects.get(id=member_id)
            GroupMember.objects.create(group=group, user=user, role='member')

        return redirect('group_chat_room', group_id=group.id)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'mxh/chat/create_chat.html', {'users': users})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import GroupChat, GroupMember, Message

@login_required
def group_chat_room(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)

    # Kiểm tra xem người dùng có là thành viên nhóm không
    if not GroupMember.objects.filter(group=group, user=request.user).exists():
        return redirect('access_denied')  # hoặc render thông báo tùy bạn

    messages = Message.objects.filter(group=group).order_by('sent_at')
    members = GroupMember.objects.filter(group=group).select_related('user')

    context = {
        'group': group,
        'messages': messages,
        'members': members,
        'username': request.user.username,
    }
    return render(request, 'mxh/chat/group_chat_room.html', context)

@login_required
def add_group_message(request, group_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        group = get_object_or_404(GroupChat, id=group_id)
        Message.objects.create(group=group, sender=request.user, content=content)
    return redirect('group_chat_room', group_id=group_id)