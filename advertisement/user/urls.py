from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='user'),
    path('verification', views.VerificationEmailView.as_view(), name='verification'),
    path('authorization', views.AuthorizedView.as_view(), name='authorization'),
    path('logout', views.logout_view, name='logout'),
    path('registration', views.RegistrationUserView.as_view(), name='registration'),
    path('update_user', views.UpdateUserView.as_view(), name='update_user'),
    path('change_password', views.MyChangePasswordView.as_view(), name='change_password'),
    path('reset_password', views.ResetPasswordView.as_view(), name='reset_password'),
    path('delete_user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('change_email', views.ChangeEmailView.as_view(), name='change_email'),
    path('user_detail/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('user_list', views.UserListView.as_view(), name='user_list'),



]
