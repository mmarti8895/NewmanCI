from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls import patterns, include, url
from dashboard import views
from dashboard import models
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ci.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.index, name='index'),
    url(r'^$', RedirectView.as_view(url='/home/')),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^user_login', views.user_login, name='user_login'),
)

handler404 = views.custom_404
handler500 = views.custom_500

urlpatterns += patterns(
        url(r'(?:.*?/)?(?P<path>(css|jquery|jscripts|js|img)/.+)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
    )
"""
# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
else:
    urlpatterns += patterns(
        url(r'(?:.*?/)?(?P<path>(css|jquery|jscripts|img)/.+)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
"""