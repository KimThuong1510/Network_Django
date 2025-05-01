from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'avatar_url']


from django import forms
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()

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

