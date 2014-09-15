from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'schwag.views.home', name='home'),
                       url(r'^about/$', 'schwag.views.about', name='about'),
                       url(r'^location/$', 'schwag.views.location', name='location'),
                       url(r'^contact/$', 'schwag.views.contact', name='contact'),
                       url(r'^bmx/$', 'schwag.views.bmx', name='bmx'),
                       url(r'^account/login/$', 'schwag.views.login', name='login'),
                       url(r'^account/logout/$', 'schwag.views.logout', name='logout'),
                       url(r'^account/register/$', 'schwag.views.register', name='register'),
                       url(r'^account/', include('django.contrib.auth.urls')),
                       url(r'^checkout/', include('senex_shop.checkout.urls')),
                       url(r'^cart/', include('senex_shop.cart.urls')),
                       url(r'^shop/', include('senex_shop.urls')),
                       url(r'^news/', include('senex_shop.news.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns += patterns('',
                                url(r'^__debug__/', include(debug_toolbar.urls)),
        )
    except ImportError:
        pass

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )