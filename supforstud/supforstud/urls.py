from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from supforstud import settings
from support.views import *

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from supforstud import settings
from support.views import *

from django.urls import path, include


class MyCustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
                      mapping={'get': 'list'},
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix': 'List'}),
        routers.Route(url=r'^{prefix}/{lookup}$',
                      mapping={'get': 'retrieve'},
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'})
    ]




router = routers.DefaultRouter()
router.register(r'support', SupportViewSet,basename='support')
print(router.urls)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('',include('support.urls')),
    # path('api/v1/', include(router.urls)),
    path('api/v1/support/', SupportAPIList.as_view()),
    path('api/v1/support/<int:pk>/', SupportAPIDetailView.as_view()),
    path('api/v1/supportdelete/<int:pk>/', SupportAPIDestroy.as_view()),

    # path('api/v1/suplist/<int:pk>', SupportAPIList.as_view()),
    # path('api/v1/supdetail/<int:pk>/', SupportAPIDetailView.as_view()),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



