"""
URL configuration for day16_02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from app01.views import depart, user, number, admin, account, order
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
from app01.utils.forms import AdminForgetForm


urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),



    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/<int:nid>/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),

    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    path('number/list/', number.number_list),
    path('number/add/', number.number_add),
    path('number/<int:nid>/edit/', number.number_edit),
    path('number/<int:nid>/delete/', number.number_delete),


    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    path('admin/logo_change/', admin.admin_logo),
    path('admin/<int:nid>/delete_confirm/', admin.admin_delete_confirm),

    path('login/', account.account_login),
    path('logout/', account.account_logout),
    path('image/code/', account.image),
    path('account/email/', account.account_RegisterEmail),
    path('sign_up/', account.sign_up),
    path('ResetPassword/', account.reset_password),
    path('account/forgetPassword/', account.reset_password_confirm),

    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/<int:nid>/delete/', order.order_delete),
    path('order/edit/', order.order_edit),
    path('order/edit/save/', order.order_editSave),


    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html', form_class=AdminForgetForm), name= 'reset_password', ),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
