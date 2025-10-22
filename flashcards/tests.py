from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from flashcards.models import FlashcardCollection, Flashcard


class FlashcardAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='strong-password',
        )
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_collection_crud_flow(self):
        # Create collection
        create_response = self.client.post(
            reverse('collection-list'),
            {'title': 'Biology', 'description': 'Study cards'},
            format='json',
        )
        self.assertEqual(create_response.status_code, 201)
        collection_id = create_response.data['id']

        # Retrieve list
        list_response = self.client.get(reverse('collection-list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        # Update
        detail_url = reverse('collection-detail', args=[collection_id])
        update_response = self.client.patch(detail_url, {'description': 'Updated'}, format='json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['description'], 'Updated')

        # Delete
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(FlashcardCollection.objects.count(), 0)

    def test_flashcard_crud_flow(self):
        collection = FlashcardCollection.objects.create(title='Physics', description='')

        # Create flashcard
        create_response = self.client.post(
            reverse('flashcard-list'),
            {
                'collection': collection.id,
                'front': 'What is the acceleration due to gravity on Earth?',
                'back': 'Approximately 9.81 m/s².',
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, 201)
        flashcard_id = create_response.data['id']

        # Filter by collection
        list_response = self.client.get(reverse('flashcard-list'), {'collection': collection.id})
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        # Update flashcard
        detail_url = reverse('flashcard-detail', args=[flashcard_id])
        update_response = self.client.put(
            detail_url,
            {
                'collection': collection.id,
                'front': 'Updated prompt',
                'back': 'Updated answer',
            },
            format='json',
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['front'], 'Updated prompt')

        # Delete flashcard
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(Flashcard.objects.count(), 0)
