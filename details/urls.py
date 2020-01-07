from django.urls import path

from . import views
from details.views import Stored

urlpatterns = [
    path('Register', views.Register, name = 'Register'),
    path('about', views.About, name = 'About'),
    path('contact', views.Contact, name = 'Contact'),
    path('term', views.Term, name = 'Term'),
    path('Login', views.Login, name = 'Login'),
    path('forgot', views.Forgot, name = 'Forgot'),
    path('main', views.Main, name = 'Main'),
    path('deposit', views.Deposit, name = 'Deposit'),
    path('transfer', views.Transfer, name = 'Transfer'),
    path('reward', views.Reward, name = 'Reward'),
    path('balance', views.Balance, name = 'Balance'),
    path('loan', views.Loan, name = 'Loan'),
    path('logout', views.Logout, name = 'Logout'),
    path('Stored', views.Stored, name = 'Stored'),







]
