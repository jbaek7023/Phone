from django.contrib.auth import login, get_user_model, logout
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, UserLoginForm
from .models import UserActivationProfile
from django.contrib import messages
from .key import (COOL_API_KEY, COOl_API_SECRET)
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

# Receive User Model
User = get_user_model()

def user_register(request, *args, **kwargs):
    '''
    Register User
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    if request.user.is_authenticated:
        raise Http404
    # Get the User Creation Form
    form = UserCreationForm(request.POST or None)
    # if the form is valid, redirect to the verifivation page
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/verify")

    context = {
        "form" : form
    }
    # Render form if the form is invalid
    return render(request, "accounts/register.html", context)


def user_login(request, *args, **kwargs):
    '''
    User Login
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return HttpResponseRedirect("/verify")
    context = {
        "form": form
    }
    # Render Login form if the form is invalid
    return render(request, "accounts/login.html", context)

def main(request, *args, **kwargs):
    '''
    Main Page : Home Page
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    if request.user.is_authenticated:
        context = {
            'login': True
        }
        return render(request, "main.html", context)
    return render(request, "main.html", {'login': False})

def user_logout(request, *args, **kwargs):
    '''
    Logout User
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    logout(request)
    return HttpResponseRedirect("/login")


def sendSMS(phone_number, activation_number):
    '''
    Send SMS message using Coolsms REST API SDK 2.0
    :param phone_number: user's phone number
    :param activation_number: activation code from user's information
    :return: None
    '''
    api_key = COOL_API_KEY
    api_secret = COOl_API_SECRET

    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
    params['to'] = phone_number  # Recipients Number '01000000000,01000000001'
    params['from'] = '01030962827'  # Sender number
    params['text'] = 'Your Verification Code: '+activation_number  # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)


def user_verify(request, *args, **kwargs):
    '''
    Verify User's Action
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    # Prevent from verifying as active user
    if request.user.is_active:
        return HttpResponseRedirect("/success_already")
    else:
        if request.method == "POST":
            code = request.POST.get("activation_key", None)
            if code is not None:
                return HttpResponseRedirect("/verify/{c}".format(c=code))
            else:
                phone_number = request.POST.get("phone_number", None)

                user_obj=User.objects.filter(phone_number=phone_number).first()
                if user_obj is None:
                    # if it's invalid number, show error message
                    messages.error(request, "Not a valid number. Try Again!")
                    return render(request, "accounts/verify.html", {"sent": False})
                else:
                    # if it's valid number, send SMS
                    # user_activation_profile = UserActivationProfile
                    activation_number = user_obj.user_activation_profile.first().key
                    sendSMS(phone_number, activation_number)

                return render(request, "accounts/verify.html", {"sent": True})
        return render(request, "accounts/verify.html", {"sent": False})


def user_activate(request, code= None,*args, **kwargs):
    '''
    Activate User
    :param request:
    :param code:
    :param args:
    :param kwargs:
    :return:
    '''
    if code is not None:
        activation_qs = UserActivationProfile.objects.filter(key=code)
        if activation_qs.exists() and activation_qs.count() == 1:
            activation_obj = activation_qs.first()

            # activation obj has user as a foreign key
            user_obj = activation_obj.user
            user_obj.is_active = True
            user_obj.save()
            return HttpResponseRedirect("/success")
        else:
            messages.error(request, "Not a valid number. Try Again!")
            return render(request, "accounts/verify.html", {"sent": True})

def success(request):
    '''
    Success Page
    :param request:
    :return:
    '''
    return render(request, "accounts/success.html")


def success_already(request):
    '''
    User is already activated
    :param request:
    :return:
    '''
    if request.user.is_authenticated:
        return render(request, "accounts/success_already.html",{})
    else:
        return Http404

