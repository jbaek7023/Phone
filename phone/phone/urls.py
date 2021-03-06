"""phone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    user_register,
    user_login,
    main,
    user_logout,
    user_verify,
    user_activate,
    success_already,
    success
)

urlpatterns = [
    url(r'^$', main, name="main"),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', user_register, name="register"),
    url(r'^login/$', user_login, name="login"),
    url(r'^logout/$', user_logout, name="logout"),
    url(r'^verify/$', user_verify, name="verify"),
    url(r'^verify/(?P<code>[0-9].*)/$', user_activate, name="activate"),
    url(r'^success_already/$', success_already, name="success_already"),
    url(r'^success/$', success, name="success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)