from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/hotels/', permanent=True)),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('hotels/', include('hotels.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
