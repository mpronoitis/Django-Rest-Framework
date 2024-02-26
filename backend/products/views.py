from rest_framework import generics,mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from api.mixins import StaffEditorPermissionMixin, UserQuerysetMixin

class ProductListCreateApiView(
     UserQuerysetMixin,
     generics.ListCreateAPIView,
     StaffEditorPermissionMixin,
     ):
     queryset = Product.objects.all()
     serializer_class = ProductSerializer
     def perform_create(self,serializer):
          title = serializer.validated_data.get('title')
          content = serializer.validated_data.get('content') or None
          if content is None:
               content = title
          if self.request.user.is_authenticated:
               serializer.save(user = self.request.user,content = content)
     # def get_queryset(self, *args, **kwargs):
     #      qs = super().get_queryset(*args, **kwargs)
     #      request = self.request
     #      print(f"Request {self.request.user}")
     #      user = request.user
     #      if not user.is_authenticated:
     #           return Product.objects.none()
     #      return qs.filter(user = request.user)
     
product_list_create_view = ProductListCreateApiView.as_view()


class ProductDetailApiView(
     UserQuerysetMixin,
     generics.RetrieveAPIView,
     StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #lookup_field = 'pk'
product_detail_view = ProductDetailApiView.as_view()

class ProductUpdateApiView(
     UserQuerysetMixin,
     generics.UpdateAPIView,
     StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def perform_update(self, serializer):
         instance = serializer.save()
         print(f"Intance is {instance}")
         if not instance.content:
              instance.content = instance.title
              
product_update_view = ProductUpdateApiView.as_view()

class ProductDestroyApiView(
     UserQuerysetMixin,
     generics.DestroyAPIView,
     StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def perform_destroy(self, instance):
         super().perform_destroy(instance)             
product_destroy_view = ProductDestroyApiView.as_view()

class ProductMixinView(
     mixins.ListModelMixin,
     mixins.RetrieveModelMixin,
     mixins.CreateModelMixin,
     mixins.DestroyModelMixin,
     mixins.UpdateModelMixin,
     generics.GenericAPIView):
     
     queryset = Product.objects.all()
     serializer_class = ProductSerializer
     #lookup_field = 'pk'
     def get(self, request, *args, **kwargs):
          print(args, kwargs)
          pk = kwargs.get('pk')
          if pk is not None:
               return self.retrieve(request, *args, **kwargs)
          return self.list(request, *args, **kwargs)
     def post(self, request, *args, **kwargs):
          return self.create(request, *args, **kwargs)
     def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content = content)
            
     def delete(self, request, *args, **kwargs):
          print(f"Request {request}")
          return self.destroy(request, *args, **kwargs)
     def update(self,request, *args, **kwargs):
          return self.update(request, *args, **kwargs)
     
product_mixin_view = ProductMixinView.as_view()
     
@api_view(http_method_names=['GET','POST'])
def product_alt_view(request,pk=None):
     method = request.method
     if method == "GET":
          if pk is not None:
               #detail View
                obj = get_object_or_404(Product, pk=pk)
                data = ProductSerializer(obj, many=False).data
                return Response(data)
            #list View
          querySet = Product.objects.all()
          data = ProductSerializer(querySet, many=True).data
          return Response(data)
     if method == "POST":
          #create item
          serializer = ProductSerializer(data=request.data)
          if serializer.is_valid(raise_exception=True):
                title = serializer.validated_data.get('title')
                content = serializer.validated_data.get('content') or None
                if content is None:
                    content = title
                serializer.save(content=content)
                return Response(serializer.data)
          return Response({"invalid": "bad data"}, status=404)
               

          
