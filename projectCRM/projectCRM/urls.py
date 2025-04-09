"""
URL configuration for projectCRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts.views import accountsViews
from accounts.views import registrationView
from accounts.views import profileView
from client.views import clientsPageViews

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('register/', registrationView, name='register'),

    path('', accountsViews, name='home'),
    path('accounts/profile/', profileView,name='profile'),
    path('clients', clientsPageViews, name='clients'),

    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('app/', include('featuredApp.urls'))

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)