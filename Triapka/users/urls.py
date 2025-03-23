from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'users'

urlpatterns = [
	path('konto/<slug:username>/', login_required(views.UserProfileView.as_view()) , name='konto'),
    path('login/', views.UserLoginView.as_view() , name='login'),
    path('logout/', views.logout , name='logout'),
    path('register/', views.UserRegistrationView.as_view() , name='register'),  
    path('update-quantity/', views.update_quantity, name='update-quantity'),
    path('ulubione/',  login_required(views.UlubioneListView.as_view()) , name='ulubione'),

    path('ustawienia/<slug:username>/', login_required(views.UserUstawieniaView.as_view()) , name='ustawienia'),
    
]