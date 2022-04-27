
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.board.views import *

# router = DefaultRouter()
# router.register('', ProductViewSet)

from rest_framework import routers
router = routers.SimpleRouter()
router.register('', PostViewSet)


urlpatterns = [
    path('', ListCreateView.as_view()),
    path('<int:pk>/', DeleteUpdateRetriveView.as_view()),
    # path('', ProductViewSet.as_view({'get':'list'})),
    path('category/', CategoryListCreateView.as_view()),
    path('category/<str:slug>/', CategoryRetriveDeleteUpdateView.as_view()),
    path('', include(router.urls)),
]