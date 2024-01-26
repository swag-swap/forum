from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model

)

User = get_user_model()

from django.contrib.auth.forms import UserCreationForm
from ...process.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='Enter your date of birth (optional)', required=False)
    profile_picture = forms.ImageField(help_text='Upload your profile picture (optional)', required=False)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'profile_picture')



class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


# class UserRegisterForm(forms.ModelForm):
#     email = forms.EmailField(label='Email address')
#     email2 = forms.EmailField(label='Confirm Email')
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'email',
#             'email2',
#             'password'
#         ]

#     def clean(self, *args, **kwargs):
#         email = self.cleaned_data.get('email')
#         email2 = self.cleaned_data.get('email2')
#         if email != email2:
#             raise forms.ValidationError("Emails must match")
#         email_qs = User.objects.filter(email=email)
#         if email_qs.exists():
#             raise forms.ValidationError(
#                 "This email has already been registered")
#         return super(UserRegisterForm, self).clean(*args, **kwargs)