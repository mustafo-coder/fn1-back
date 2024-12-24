from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from django.db.models import Q

# GET uchun Login Required bo'lmagan API
class ArticleListAPIView(APIView):
    permission_classes = [AllowAny]  # Login talab qilinmaydi

    def get(self, request):
        # Qidiruv so'rovini olish
        search_query = request.query_params.get('search', None)

        # Qidiruv bo'lsa, filtrlash
        if search_query:
            articles = Article.objects.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        else:
            articles = Article.objects.all()

        # Serializer yaratish va javob qaytarish
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Login talab qilinadi

    def post(self, request):
        # Serializerga rasmni va boshqa ma'lumotlarni yuborish
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # Rasmni saqlash
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE uchun Login Required API
class ArticleUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Login talab qilinadi

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE uchun Login Required API
class ArticleDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def delete(self, request, pk, format=None):
        try:
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response({'message': 'Article deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

class ArticleRetrieveAPIView(APIView):
    permission_classes = [AllowAny]  # Login talab qilinmaydi

    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serializer yaratish va maqolani javob sifatida qaytarish
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

class ArticleSearchAPIView(APIView):
    permission_classes = [AllowAny]  # Login talab qilinmaydi

    def get(self, request):
        query = request.GET.get('query', '')
        if not query:
            return Response({"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Qidiruvni amalga oshirish
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(author__icontains=query)
        )

        if not articles.exists():
            return Response({"message": "No articles found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)