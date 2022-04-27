
from django.urls import path, include

from applications.account.views import *


urlpatterns = [
    path('register/' ,RegisterAPIView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutView.as_view()),

]