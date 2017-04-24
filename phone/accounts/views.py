from django.shortcuts import render

from .forms import UserCreationForm, UserChangeForm

# Create your views here.
def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        print("user has been created")
    context = {
        "form" : form
    }
    return render(request, "accounts/register.html", context)