from django import forms
from .models import CustomUser

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiya'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '998901234567'}),
        }
