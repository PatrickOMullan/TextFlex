from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    Banner_Password = forms.CharField(help_text='Required. Must be exactly your bannerweb password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'Banner_Password',]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    Banner_Password = forms.CharField(help_text='Required. Must be exactly your bannerweb password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

'''
def register(request):
    if request.metho == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user
'''