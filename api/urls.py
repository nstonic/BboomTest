from rest_framework.routers import DefaultRouter

from .views import PostViewSet, UserViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
