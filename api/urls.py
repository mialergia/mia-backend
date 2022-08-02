from django.urls import include, path

from users.views import CustomTokenRefreshView

urlpatterns = [
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('', include('dj_rest_auth.urls')),
    path('users/', include('users.urls')),
    path('symptoms/', include('symptoms.urls')),
    path('pollens/', include('pollens.urls')),
    path('information/', include('information.urls')),
]
