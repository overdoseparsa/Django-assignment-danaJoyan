from django.urls import include, path

from dana.users.urls import urlpatterns as user_urlpatterns

urlpatterns = [
    path("users/", include(user_urlpatterns)),
]
