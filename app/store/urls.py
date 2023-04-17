from django.urls import path
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, BookGPViewSet

router = SimpleRouter()
router.register('gp', BookGPViewSet, basename='gp')
router.register('book', BookViewSet)

urlpatterns = [
    # path()
]

urlpatterns += router.urls
print(f"urls: {urlpatterns}")

# browser URL /store/book/?format=json