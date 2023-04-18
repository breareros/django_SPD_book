from django.urls import path, include
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, BookGPViewSet

router = SimpleRouter()
router.register(r'api/gp', BookGPViewSet, basename='gp')
router.register(r'api/book', BookViewSet)


urlpatterns = [
    # path()
    # path('', include('django.contrib.auth.urls')),
]

urlpatterns += router.urls
urlpatterns += [path('', include('django.contrib.auth.urls')),]
# print(f"urls: {urlpatterns}")

# browser URL /store/book/?format=json