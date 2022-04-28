import django_filters
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets

from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet

from applications.board.filters import ProductFilter
from applications.board.models import *

# from applications.telebot.sendmessage import sendTelegram
from applications.board.permissions import IsAdmin
from applications.board.serializers import *


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListCreateView(ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # IsAdminUser
    # pagination_class = None
    pagination_class = LargeResultsSetPagination

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category','sub_category','price','city']
    search_fields = ['name','description']
    # filterset_class = ProductFilter
    ordering_fields = ['id', 'price']


    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['id','price']
    search_fields = ['name','description']

    def get_permissions(self):
        print(self.action)
        if self.action in ['list','retrieve']:
            permissions = []
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


#review
    @action(methods=['POST'], detail=True)
    def review(self, request, pk):
        serializer = ReviewSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Review.objects.get(post=self.get_object(),
                                      owner=request.user)
            obj.review = request.data['review']
        except Review.DoesNotExist:
            obj = Review(owner=request.user,
                          post=self.get_object(),
                          )
        obj.save()
        return Response(request.data,
                        status=status.HTTP_201_CREATED)


##Likes
    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        obj = Likes.objects.filter(post=self.get_object(), owner=request.user)
        if obj:
            obj.delete()
            return Response('unliked')
        obj = Likes.objects.create(owner=request.user, post=self.get_object())
        obj.save()
        return Response('liked')

##Favorites
    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk):
        serializer = FavoriteSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            object = Favorite.objects.get(post=self.get_object(),owner=request.user)
        except Favorite.DoesNotExist:
            object = Favorite(owner=request.user,post=self.get_object())
        object.save()
        return Response('Добавлено в избранное', status=status.HTTP_200_OK)

##rating
    @action(methods=['POST'], detail=True)
    def rating(self, request, pk):
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Rating.objects.get(post=self.get_object(), owner=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(owner=request.user, post=self.get_object(), rating=request.data['rating'])
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)




class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdmin]

class CategoryRetriveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdmin]


class DeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] # [IsAdmin]




##Order
#     @action(methods=['POST'], detail=True)
#     def order(self, request, pk):
#         serializer = OrderSerializers(data=request.data)
#         obj = Order.objects.create(product=self.get_object(), customer=request.data['customer'],
#                                 tel = request.data['tel'], quantity = request.data['quantity'])
#         obj.save()
#         vl = obj.product_id
#         # print(vl)
#         objquery = request.data.copy()
#         objquery.__setitem__("product_id", vl)
#         tg_prod = str(Product.objects.get(pk=vl))
#         # print(tg_prod)
#         #
# ##TeleBot
#         sendTelegram(tg_customer=obj.customer, tg_tel=obj.tel,tg_prod = tg_prod, tg_qty = obj.quantity )
#
#         return Response(objquery,
#                         status=status.HTTP_201_CREATED)