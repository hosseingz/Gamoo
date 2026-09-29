from rest_framework import generics, permissions
from blog.models import Post
from .serializers import PostListSerializer, PostDetailSerializer

class PostListView(generics.ListAPIView):
    """
    API view to list all published blog posts.
    Optimized with select_related to avoid N+1 queries.
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author')

class PostDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a published blog post by slug.
    Optimized with select_related to avoid N+1 queries.
    """
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author')
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
