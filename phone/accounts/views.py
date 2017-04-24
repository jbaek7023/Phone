from django.contrib.auth import login, get_user_model, logout
from django.http import Http404
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
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        # if request.user.is_authenticated:
        #     print("Login Successful")
        return HttpResponseRedirect("/")

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)

def main(request):
    if request.user.is_authenticated:
        context = {
            'login': True
        }
    return render(request, "main.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

def user_verify(request):
    if not request.user.is_authenticated:
        return Http404
    else:

        return render(request, "verify.html". context)