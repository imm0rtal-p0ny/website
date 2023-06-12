from django.contrib.auth.forms import forms, AuthenticationForm, UserChangeForm, UserCreationForm
from django.utils.crypto import get_random_string
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class EmailVerificationForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=5)


class RegistrationUserForm(forms.ModelForm):
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        exclude = [
            'last_login',
            '_code',
            'is_active',
            'is_superuser',
            'is_staff',
            'is_authorized',
            'groups',
            'user_permissions',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('repeat_password')
        if password1 != password2:
            self.add_error('repeat_password', 'Passwords do not match')
            self.add_error('password', 'Passwords do not match')

        return cleaned_data


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'middle_name',

        ]


class ResetPasswordInEmailForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    code = forms.CharField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password')
        password2 = cleaned_data.get('repeat_password')
        if password1 != password2:
            self.add_error('repeat_password', 'Passwords do not match')
            self.add_error('new_password', 'Passwords do not match')

        return cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(required=False)



