from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [ 
    path('',views.home,name='home'),
    path('addpost/',views.addpost,name='addpost'),
    path('register/',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('post/<int:pk>/',views.post_d,name='post'),
    path('forgot_password/',views.ForgotPassword,name='forgot_password'),
    path('change_password/<str:username>/<token>/',views.ChangePassword,name='change_password'),
    path('contact_us/',views.Contact_Us,name='contact_us'),
    path('about_us/',views.About_Us,name='about_us'),
    path('search_post/',views.Search_Post,name='search_post'),
    path('logged_in_user_posts/',views.MyPost,name='logged_in_user_posts'),
    path('edit_post/<pk>/',views.EditPost,name='edit_post'),
    path('email_verification/',views.EmailVerification,name='email_verification'),
    path('otp_verification/<str:email>/',views.OtpVerification,name='otp_verification'),
    path('like_post/<int:pk>/',views.LikePost,name='like_post'),
    path('post/<int:pk>/comment',views.AddComment,name='addcomments'),

    # path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    # path('paaword_reset/done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('password_reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # path('password_reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]