"""
URL configuration for openplaza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from core import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),                                                                              # homepage
    path("logout/", views.logout_view, name="logout"),                                                                  # logout
    path("login/", views.login_view, name="login"),                                                                     # login
    path("register/", views.register_view, name="register"),                                                            # registrazione
    path("check_username_availability/", views.check_username_availability, name="check_username_availability"),        # controlla che l'username sia disponibile
    path("product/create/", views.create_product, name="create_product"),                                               # vendi
    path('product/<int:id>/', views.product_detail, name='product_detail'),                                             # dettagli prodotto
    path('search/', views.search_results_view, name='search_results'),                                                  # ricerca prodotti
    path('test/', views.test_view, name="test"),
    path('user/<str:username>/', views.user_profile_view, name="user_profile"),                                         #! Questa url deve rimanere per ultimo
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
