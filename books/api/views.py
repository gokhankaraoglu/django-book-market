# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from books.api.serializers import BookSerializer, CommentSerializer
from books.models import Book, Comment
from books.api.permissions import IsAdminUserReadOnly, IsCommentByOrReadOnly

class BookListCreateAPIView(generics.ListCreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAdminUserReadOnly]


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAdminUserReadOnly]


class CommentCreateAPIView(generics.CreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [IsAdminUserReadOnly]
  


  def perform_create(self, serializer):
    book_pk = self.kwargs.get('book_pk')
    book = get_object_or_404(Book, pk=book_pk)
    comment_by = self.request.user

    comments = Comment.objects.filter(book=book, comment_by=comment_by) 
    if comments.exists():
      raise ValidationError('You commented a book before.')

    serializer.save(book=book, comment_by = comment_by)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [IsCommentByOrReadOnly]





# class BookListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
#   queryset = Book.objects.all()
#   serializer_class = BookSerializer


#   # List
#   def get(self, request, *args, **kwargs):
#     return self.list(request, *args, **kwargs)

#   # Create
#   def post(self, request, *args, **kwargs):
#     return self.create(request, *args, **kwargs)