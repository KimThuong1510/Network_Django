from django import forms
from .models import Post
from django import forms
from django.contrib.auth import get_user_model
from .models import Department, GroupChat

User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'avatar_url']
        labels = {
            'title': '',
            'avatar_url': 'Hình ảnh đính kèm',
        }
        widgets = {
            'title': forms.Textarea(attrs={
                'placeholder': 'Nhập nội dung bài viết',
                'class': 'form-control',
                'rows': 4
            }),
            'avatar_url': forms.URLInput(attrs={
                'placeholder': 'Nhập URL hình ảnh',
                'class': 'form-control'
            }),
        }


class EmployeeSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Tìm kiếm',
        widget=forms.TextInput(attrs={'placeholder': 'Tìm theo tên...'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label='Bộ phận',
        empty_label='Tất cả bộ phận'
    )

class CreateGroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Chọn thành viên'
    )

    class Meta:
        model = GroupChat
        fields = ['group_name', 'members']

