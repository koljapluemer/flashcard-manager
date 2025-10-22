from rest_framework.routers import DefaultRouter

from flashcards.api.views import FlashcardCollectionViewSet, FlashcardViewSet

router = DefaultRouter()
router.register('collections', FlashcardCollectionViewSet, basename='collection')
router.register('flashcards', FlashcardViewSet, basename='flashcard')

urlpatterns = router.urls
