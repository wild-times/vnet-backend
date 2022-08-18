from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from meeting.views import MainMeetingView

urlpatterns = [
    path('admin/', admin.site.urls),

    # help/
    path('help/', include('help.urls')),

    # core/
    path('core/', include('core.urls')),

    # meeting/
    path('meeting/', include('meeting.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    re_path(r'meet/(?P<path>.*)', MainMeetingView.as_view(), name='meeting-main'),
]
