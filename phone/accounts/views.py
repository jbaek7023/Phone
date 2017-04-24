from django.contrib.auth import login, get_user_model, logout
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, UserChangeForm, UserLoginForm
from .models import UserActivationProfile

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

def main(request, *args, **kwargs):
    if request.user.is_authenticated:
        context = {
            'login': True
        }
    return render(request, "main.html", context)

def user_logout(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect("/login")

# Login Required
def user_verify(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Http404
    else:
        if request.method == "POST":
            # Send CoolSMS
            # sendCoolSMS()
            code = request.POST.get("activation_key", None)
            print(code)
            activation_qs = UserActivationProfile.objects.filter(key=code)
            if activation_qs.exists() and activation_qs.count() ==1:
                activation_obj = activation_qs.first()

                # activation obj has user as a foreign key
                user_obj = activation_obj.user
                user_obj.is_active = True
                user_obj.save()

            return render(request, "accounts/verify.html", {"sent" : True})
        return render(request, "accounts/verify.html", {"sent": False})

def sendCoolSMS(self):
    pass
