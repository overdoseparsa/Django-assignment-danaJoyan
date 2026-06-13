from django.urls import include, path

from dana.trasnport.urls import urlpatterns as transport_urlpatterns
from dana.users.urls import urlpatterns as user_urlpatterns

urlpatterns = [
    path("users/", include(user_urlpatterns)),
    path("transport/", include(transport_urlpatterns)),
]
