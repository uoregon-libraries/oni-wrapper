from django.conf.urls import url, include

urlpatterns = [
    url('', include("themes.oregon.urls")),
    url(r'^map$', include("onisite.plugins.map.urls")),
    url('', include("onisite.plugins.calendar.urls")),
    url('', include("core.urls")),
    url('', include("onisite.plugins.staticpages.urls")),
]
