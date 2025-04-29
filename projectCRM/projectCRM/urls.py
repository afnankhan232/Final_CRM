"""
Important Link(s):
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

from django.conf import settings
from django.conf.urls.static import static

# Views from Different django-apps
from accounts.views import indexView
from accounts.views import aboutView
from accounts.views import registrationView
from accounts.views import profileView
from client.views import clientsPageViews

# for Authentication - Login and Logout
from django.contrib.auth import views as auth_views

# URL's!
urlpatterns = [

    # Index / Home Page
    path('', indexView, name='index'),
    path('home/', indexView, name='home'),
    path('about/', aboutView, name='about'),

    # Creating New User (Registration Page)
    path('register/', registrationView, name='register'),

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Profile View [Temporary]
    path('accounts/profile/', profileView, name='profile'),

    # This should be removed!
    path('clients', clientsPageViews, name='clients'), 

    # Admin Page for Local Development
    path('admin/', admin.site.urls),
    

    # Advanced Featured App
    path('apps/', include('featuredApp.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)