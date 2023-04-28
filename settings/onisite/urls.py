from django.urls import include, path, re_path

urlpatterns = [
    path('', include("themes.oregon.urls")),
    re_path(r'^map$', include("onisite.plugins.map.urls")),
    path('', include("onisite.plugins.calendar.urls")),
    path('', include("core.urls")),
    path('', include("onisite.plugins.staticpages.urls")),
]
