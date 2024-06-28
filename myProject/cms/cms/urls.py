from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cmsapp.urls'))
]

urlpatterns += static(settings.IMAGE_URL, document_root = settings.IMAGE_ROOT)
