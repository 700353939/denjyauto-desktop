from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from denjyauto.accounts.views.restView import LoginClientsUserView, LogoutClientsUserView, ClientChangePasswordView
from denjyauto.reprForClients.views import CarViewSet, RepairViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'repairs', RepairViewSet)

urlpatterns = [
    path('swagger-ui', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('login/', LoginClientsUserView.as_view(), name='login-clients'),
    path('logout/', LogoutClientsUserView.as_view(), name='logout-clients'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', ClientChangePasswordView.as_view(), name='change-password-clients'),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include(router.urls)),
]