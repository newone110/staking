from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error/', views.error, name='error'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('connect/', views.connect, name='connect'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fund/', views.fund, name='fund'),
    path('market/', views.market, name='market'),
    path('stake/', views.stake, name='stake'),
    path('pay/', views.pay, name='pay'),
    path('signout/', views.signout),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('learn/', views.stake_view, name='learn'),
    path('admin-signin/', views.admin_signin, name='admin-signin'),
    path('admin-withdraw/', views.admin_withdraw, name='admin-withdraw'),
]