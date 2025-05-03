from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # Các trường hiển thị trong phần list view
    list_display = (
    'username', 'first_name', 'last_name', 'email', 'role', 'phone', 'birth_date', 'gender', 'department', 'is_active')

    # Các trường trong form chỉnh sửa người dùng
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'avatar_url')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Các trường trong form tạo mới người dùng
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'avatar_url', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Trường tìm kiếm trong Admin
    search_fields = ('username', 'first_name', 'last_name', 'email', 'role')

    # Các trường lọc
    list_filter = ('role', 'is_active', 'is_staff')


# Đăng ký model với Admin
admin.site.register(User, CustomUserAdmin)
