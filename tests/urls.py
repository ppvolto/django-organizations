from django.conf.urls import include, url
from django.contrib import admin

# from organizations.backends import invitation_backend, registration_backend
from organizations.settings import organizations_settings 
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^invite/', include(organizations_settings.INVITATION_BACKEND().get_urls())),
    url(r'^register/', include(organizations_settings.REGISTRATION_BACKEND().get_urls())),
]
