from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permission
from django.conf import settings
from django.conf.urls.static import static
from users.views import activate_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('no-permission/', no_permission, name='no-permission'),
    path('users/', include('users.urls')),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('events/', include('event.urls')),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
