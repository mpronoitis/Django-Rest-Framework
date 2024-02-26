from rest_framework import serializers


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)


    # def get_other_products(self,obj):
    #     request = self.context.get('request')
    #     print(f"Request is {request}")
    #     my_products_qs = obj.product_set.all() #find all the related products of the user
    #     return UserProductInlineSerializer(my_products_qs, many=True, context = self.context).data