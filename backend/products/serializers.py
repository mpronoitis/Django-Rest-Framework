from rest_framework import serializers,validators
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title_no_hello,unique_product_title
from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'pk',
        read_only=True
        )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
   # related_products = ProductInlineSerializer(source='user.products',many=True, read_only=True)
   # my_discount = serializers.SerializerMethodField(read_only=True)
    #my_user_data = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'pk'
        )
    class Meta:
        model = Product
        fields = [
            'pk',
            'owner',
            'title',
            'edit_url',
            'url',
            'content',
            'price',
            'sale_price',
            'public'
        ]
    title = serializers.CharField(validators={validate_title_no_hello, unique_product_title})
    # def validate_title(self,value):
    #     request = self.context.get('request')
    #     user = request.user
    #     print(f"Self {self}")
    #     print(f"\nRequest {request} and User {user}")
    #     qs = Product.objects.filter(title__exact = value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    def get_my_user_data(self,obj):
        return {
            'username':obj.user.username
        }
    def get_my_discount(self,obj):
         if not hasattr(obj, 'id'):
             return None
         if not isinstance(obj, Product):
            return None
         return obj.get_discount()
    
    def get_edit_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk":obj.pk}, request = request)
