from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Views from accounts
from accounts.views import indexView
from accounts.views import aboutView

# for Authentication - Login and Logout
from django.contrib.auth import views as auth_views

# URL's!
urlpatterns = [

    # Index / Home Page [WELCOME PAGE]
    path('', indexView, name='index'),
    path('home/', indexView, name='home'),
    path('about/', aboutView, name='about'),

    path("accounts/", include("allauth.urls")),

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Admin Page for Local Development
    path('admin/', admin.site.urls),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)