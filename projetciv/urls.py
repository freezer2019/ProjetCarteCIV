from django.urls import path, include
from . import views
from .import AdminManagerViews, PlateformManagerViews, ManagerViews


urlpatterns = [
    path('', views.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    #path('admin_home/', HodViews.admin_home, name="admin_home"),
]