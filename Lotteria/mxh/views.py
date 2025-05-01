from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Max, F, OuterRef, Subquery
from django.utils import timezone
from .models import PrivateChat, PrivateMessage, Friend
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
    return render(request, 'mxh/Login/login.html')

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

    comments = Comment.objects.all()  # Lấy tất cả bình luận
    posts = Post.objects.all().order_by('-created_at')  # Lấy tất cả bài viết

    context = {
        'form': form,
        'posts': posts,
        'comments': comments,
    }

    return render(request, 'mxh/Home/Home.html', context)

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
    return render(request, 'mxh/Home/Home.html', context)

# Tìm kiếm tên và bộ phận
from django.contrib.auth import get_user_model
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
    return render(request, 'search_employees.html', context)

# Chat tin nhắn cá nhân

logger = logging.getLogger(__name__)
User = get_user_model()

@login_required
def api_get_or_create_chat(request, user_id):
    try:
        other_user = User.objects.get(id=user_id)

        is_friend = Friend.objects.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(receiver=request.user) & Q(sender=other_user))
        ).exists()

        if not is_friend:
            return JsonResponse({
                'status': 'error',
                'message': 'Bạn chưa kết bạn với người dùng này'
            }, status=400)

        chat = PrivateChat.objects.filter(
            (Q(user1=request.user) & Q(user2=other_user)) |
            (Q(user2=request.user) & Q(user1=other_user))
        ).first()


        if not chat:
            chat = PrivateChat.objects.create(
                user1=request.user,
                user2=other_user
            )
            logger.info(f"Created new chat: {chat.id} between {request.user.username} and {other_user.username}")

        receiver = chat.get_receiver(request.user)
        return JsonResponse({
            'status': 'success',
            'chat': {
                'id': chat.id,
                'created_at': chat.created_at.isoformat()
            },
            'receiver': {
                'id': receiver.id,
                'name': f"{receiver.first_name} {receiver.last_name}",
                'avatar_url': receiver.avatar_url
            }
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Người dùng không tồn tại'
        }, status=404)


@login_required
def api_get_messages(request, chat_id):
    try:
        chat = get_object_or_404(
            PrivateChat,
            Q(user1=request.user) | Q(user2=request.user),
            id=chat_id
        )
        messages = PrivateMessage.objects.filter(chat=chat).order_by('sent_at')

        message_list = []
        for msg in messages:
            message_list.append({
                'id': msg.id,
                'content': msg.content,
                'is_sender': msg.sender == request.user,
                'sent_at': msg.sent_at.isoformat()
            })

        return JsonResponse({
            'status': 'success',
            'messages': message_list
        })
    except PrivateChat.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Cuộc trò chuyện không tồn tại hoặc bạn không có quyền truy cập'
        }, status=404)


@login_required
def api_send_message(request):
    try:
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        content = data.get('content')

        if not chat_id or not content:
            return JsonResponse({
                'status': 'error',
                'message': 'Thiếu thông tin cần thiết'
            }, status=400)

        chat = PrivateChat.objects.filter(
            Q(user1=request.user) | Q(user2=request.user),
            id=chat_id
        ).first()

        if not chat:
            return JsonResponse({
                'status': 'error',
                'message': 'Cuộc trò chuyện không tồn tại hoặc bạn không có quyền truy cập'
            }, status=404)

        message = PrivateMessage.objects.create(
            chat=chat,
            sender=request.user,
            content=content
        )

        logger.info(f"Message saved to database: ID={message.id}, Content={message.content}")

        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'sent_at': message.sent_at.isoformat()
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Lỗi: {str(e)}'
        }, status=500)



@login_required
def api_get_chats(request):
    chats = PrivateChat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )

    chat_list = []
    for chat in chats:
        receiver = chat.get_receiver(request.user)
        last_message = PrivateMessage.objects.filter(chat=chat).order_by('-sent_at').first()

        chat_list.append({
            'id': chat.id,
            'receiver': {
                'id': receiver.id,
                'name': f"{receiver.first_name} {receiver.last_name}",
                'avatar_url': receiver.avatar_url
            },
            'last_message': {
                'content': last_message.content if last_message else None,
                'sent_at': last_message.sent_at.isoformat() if last_message else None
            }
        })

    chat_list.sort(
        key=lambda x: x['last_message']['sent_at'] if x['last_message'] and x['last_message']['sent_at'] else '0',
        reverse=True)

    return JsonResponse({
        'status': 'success',
        'chats': chat_list
    })


@login_required
def api_send_friend_request(request):
    try:
        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')
        if not receiver_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Thiếu ID người nhận'
            }, status=400)

        receiver = User.objects.get(id=receiver_id)

        is_friend = Friend.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) |
            (Q(receiver=request.user) & Q(sender=receiver))
        ).exists()

        if is_friend:
            return JsonResponse({
                'status': 'error',
                'message': 'Đã là bạn bè'
            }, status=400)

        friend = Friend.objects.create(
            sender=request.user,
            receiver=receiver
        )

        logger.info(f"Friend request created: {friend.id} from {request.user.username} to {receiver.username}")

        return JsonResponse({
            'status': 'success'
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Người dùng không tồn tại'
        }, status=404)
    except Exception as e:
        logger.error(f"Error sending friend request: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Lỗi: {str(e)}'
        }, status=500)
