from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator
from django.db.models import Q

from .models import USERNAME_REGEX

# Get User Model
User = get_user_model()

class UserLoginForm(forms.Form):
    '''
    User LoginForm
    '''
    username = forms.CharField(
        label= 'User Name',
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be Alpahnumeric or contain any of the following: ". @ + -" ',
                code='invalid_username'
            )])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **Kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # Built in Authentication

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            raise forms.ValidationError("Invalid username or password.")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError("Invalid username or password.")
            # if not user_obj.is_active:
            #     raise forms.ValidationError("Inactive user; Please verify your account using SMS!")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **Kwargs)



# REFERENCE: Django Documentation
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email.



        if commit:
            user.save()
        return user
