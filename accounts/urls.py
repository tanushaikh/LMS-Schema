from django.urls import path
from .views import RegisterView, LoginView,UserDetailView,LogoutView
from .views import RoleViewSet, PermissionViewSet, RolePermissionViewSet,ProfileViewSet,PostViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'role-permissions', RolePermissionViewSet, basename='role-permission')
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path("logout/", LogoutView.as_view(), name="logout"),


]