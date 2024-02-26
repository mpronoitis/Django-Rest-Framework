from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.
from . import client
class SearchListView(generics.GenericAPIView):
     def get(self, request, *args, **kwargs):
          user = None
          if request.user.is_authenticated:
               user = request.user.username
          query = request.GET.get('q')
          public = str(request.GET.get('public')) != "0"
          tag = request.GET.get('tag')
          if not query:
               return Response('',status=400)
          results = client.perform_search(query, tags = [tag] if tag else [], user = user, public = public)
          return Response(results)

class SearchListOldView(generics.ListAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

        def get_queryset(self, *args, **kwargs):
            # use the search method from the ProductManager
            qs = super().get_queryset(*args, **kwargs)
            q = self.request.GET.get('q')
            results = Product.objects.none()
            if q is not None:
                user = None
                if self.request.user.is_authenticated:
                    user = self.request.user
                results = qs.search(query = q, user = user)
            return results
                
           

search_list_view = SearchListView.as_view()

 