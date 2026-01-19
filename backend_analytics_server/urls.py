from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard.views import index

handler403 = 'dashboard.views.custom_permission_denied'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='security/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]
