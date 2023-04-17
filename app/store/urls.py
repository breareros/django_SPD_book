from django.urls import path
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, BookGPViewSet

router = SimpleRouter()
router.register(r'gp', BookGPViewSet, basename='gp')
router.register(r'book', BookViewSet)

urlpatterns = [
    # path()
]

urlpatterns += router.urls
# print(f"urls: {urlpatterns}")

# browser URL /store/book/?format=json