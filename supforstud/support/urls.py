from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', SupportHome.as_view(),name='home'),
    path('about/',about,name='about'),
    path('news/', news, name='news'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', SupportCategory.as_view(), name='category'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404=pageNotFound
handler403=Forbidden
handler400=BadRequest
handler500=ServerError