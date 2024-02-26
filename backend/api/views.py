from django.http import JsonResponse,HttpResponse
from django.forms.models import model_to_dict
import json
from products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer

@api_view(http_method_names=['POST'])
def api_home(request):
   
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        # print(instance)
        return Response(serializer.data)
    return Response({"invalid":"Not good data"})


#JsonResponse as data must be a dictionary
#HttpResponse wait for a dummy string as data json_data_str = json.dumps(data)