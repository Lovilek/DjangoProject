from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from supforstud import settings
from support.views import *

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from supforstud import settings
from support.views import *

from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('',include('support.urls')),
    path('api/v1/suplist/', SupportAPIView.as_view()),
    path('api/v1/suplist/<int:pk>', SupportAPIView.as_view()),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



