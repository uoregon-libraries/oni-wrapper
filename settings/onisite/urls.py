from django.conf.urls import url, include

urlpatterns = [
    url('', include("themes.oregon.urls")),
    url('^static/', include("onisite.plugins.staticpages.urls")),
    url(r'^map$', include("onisite.plugins.map.urls")),
    url(r'^$', include("onisite.plugins.featured_content.urls")),
    url('', include("core.urls")),
]
