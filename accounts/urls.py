from django.urls import path
from .views import login_signup_view, signup_user, logout_user, login_user

urlpatterns = [
    path('', login_signup_view, name='accounts'),
    path('signup/', signup_user, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
