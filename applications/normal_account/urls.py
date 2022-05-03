from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from applications.normal_account.views import *



urlpatterns = [
    path('register/' ,RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutView.as_view()),

    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', CompleteResetPassword.as_view()),

]