from django.contrib import admin
from django.urls import include, path

from homepage.views import HomeView
from marketplace.views import MarketplaceView

from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('auth/', include('users.urls')),
    path('marketplace/', MarketplaceView.as_view())
]

if DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
