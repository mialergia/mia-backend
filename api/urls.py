from django.urls import include, path

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('users/', include('users.urls')),
    path('symptoms/', include('symptoms.urls')),
    path('pollens/', include('pollens.urls')),
    path('information/', include('information.urls')),
]
