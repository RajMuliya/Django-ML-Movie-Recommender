# # forms.py

# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User

# class RegistrationForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=150)
#     email = forms.EmailField(label='Email Address')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get('username'),
#         email = cleaned_data.get('email'),
#         password = cleaned_data.get('password'),
#         confirm_password = cleaned_data.get('confirm_password'),

#         if username.lower() in ['admin', 'root', 'superuser']:
#             self.add_error('username','username already occupied')
        
    


# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username111'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    
    
    # Custom validation for username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.lower() in ['admin', 'root', 'superuser']:
            raise ValidationError("This username is reserved and cannot be used.")
        return username
    
    # Custom validation for email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use. Please use a different one.")
        return email

    # Custom validation for password1 (and confirm password matching)
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Custom password requirements (example)
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
        
        return password1

    # Custom validation for password2 (confirm password matching)
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if both passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        
        return password2

    # Custom validation for the entire form (if needed)
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        # Example: Check if the first name and last name are the same
        if first_name and last_name and first_name.lower() == last_name.lower():
            raise ValidationError("First name and last name cannot be the same.")

        return cleaned_data
    

from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))