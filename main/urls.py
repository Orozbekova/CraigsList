from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from applications.chat_app import views
from main import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('applications.board.urls')),
    path('account/', include('applications.normal_account.urls')),
    path('swagger/', schema_view.with_ui('swagger')),
    path('cart/', include('applications.cart.urls')),
    path('chat/', include('applications.chat_app.urls')),
    path('',TemplateView.as_view(template_name='/home/umutai/Desktop/makers/CraigsList/applications/normal_account/templates/login.html')),
    path('accounts/',include('allauth.urls')),
    # path('api/v1/product', include('applications.product.urls')),
    # path('api/v1/account/', include('applications.account.urls')),

              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
