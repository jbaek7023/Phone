from django.contrib.auth import login, get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, UserChangeForm, UserLoginForm

User = get_user_model()

# Create your views here.
def user_register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/login")

    context = {
        "form" : form
    }
    return render(request, "accounts/register.html", context)


def user_login(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=user_name)
        login(request, user_obj)
        if request.user.is_authenticated:
            print("Login Successful")
        return HttpResponseRedirect("/")

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)