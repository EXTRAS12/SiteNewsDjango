from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('authenticate.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
    ]+urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
