from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import SocketAuthView
from homepage.views import HomeView
from stock_exchange import settings

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('', HomeView.as_view()),
        path('auth/', include('users.urls')),
        path('marketplace/', include('marketplace.urls')),
        path('tinymce/', include('tinymce.urls')),
        path('companies/', include('companies.urls')),
        path('socket-auth/', SocketAuthView.as_view()),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
