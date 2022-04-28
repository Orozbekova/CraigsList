from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    path('account/', include('applications.account.urls')),
    path('swagger/', schema_view.with_ui('swagger')),
    path('cart/', include('applications.cart.urls'))
    # path('api/v1/product', include('applications.product.urls')),
    # path('api/v1/account/', include('applications.account.urls')),

              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
