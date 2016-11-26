from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import keystamp_crypto.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', keystamp_crypto.views.index, name='index'),
    url(r'^hashme$', keystamp_crypto.views.hashme, name='hashme'),

#    url(r'^listdocs', keystamp_crypto.views.list, name='list'),

    # url(r'^db', hello.views.db, name='db'),
   # url(r'^admin/', include(admin.site.urls)),
]