from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserCreationForm, UserChangeForm, UserLoginForm

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
        # form.save()
        return HttpResponseRedirect("/")

    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)