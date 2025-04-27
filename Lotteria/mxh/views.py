from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Comment

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
    return render(request, 'mxh/Home/Home.html')


@login_required
def admin_home(request):
    return render(request, 'mxh/Chat/Chat_admin.html')


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

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'mxh/Home/Home.html', {'form': form, 'posts': posts})

@login_required
def task_view(request):
    return render(request, 'mxh/Task/Task.html')

@login_required
def chat_view(request):
    return render(request, 'mxh/Chat/Chat.html')

@login_required
def company_view(request):
    return render(request, 'mxh/Nofication/Company.html')

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
    return render(request, 'mxh/Home/Create_post.html', {'form': form})

# Bình luận
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment


from django.shortcuts import render, get_object_or_404
from .models import Post, Comment

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Thêm bình luận vào cơ sở dữ liệu
            Comment.objects.create(post=post, user=request.user, content=content)

    # Sau khi thêm bình luận, render lại trang chi tiết bài viết với bình luận mới
    return redirect('post_detail', post_id=post.id)


from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'mxh/Home/post_detail.html', {'post': post})
