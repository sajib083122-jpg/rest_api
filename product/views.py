import random
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Book
from product.serializers import BookSerializer
from rest_framework import status


# Create your views here.

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book_slug = serializer.validated_data.get('book_name').lower().replace(' ', '-')
            random_number = random.randint(10000, 99999)  # Generate a random number based on the count of existing books
            unique_slug  = f"{book_slug}-{random_number}"  # Append the random number to
            serializer.save(slug=unique_slug)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    def get_object(self, slug):
        try:
            return Book.objects.get(slug=slug)
        except Book.DoesNotExist:
            return None

    def get(self, request, slug):
        book = self.get_object(slug)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, slug):
        book = self.get_object(slug)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        book = self.get_object(slug)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    