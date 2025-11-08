from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User # type: ignore
from django import forms # type: ignore
from .models import Profile

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full border border-[#68c2ef] rounded-lg p-2 text-black'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-[#68c2ef] rounded-lg p-2 text-black'}),
            'password1': forms.PasswordInput(attrs={'class': 'w-full border border-[#68c2ef] rounded-lg p-2 text-black'}),
            'password2': forms.PasswordInput(attrs={'class': 'w-full border border-[#68c2ef] rounded-lg p-2 text-black'}),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'w-full border border-[#68c2ef] rounded-lg p-2'}),
        }