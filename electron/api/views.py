from rest_framework import generics
from store.models import Product
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms import model_to_dict


class ProductsAPIView(APIView):
    def get(self, request):
        products = list(Product.objects.all().values())
        return Response(products)

    # def post(self, request):
    #     # keys = ("image", "name", "product_slug", "category_id", "price", "description", "quantity", "discount")
    #     # values = []
    #     # for key in keys:
    #     #     try:
    #     #         values.append(request.data[key])
    #     #     except KeyError:
    #     #         return Response({'created': False,
    #     #                          'message': 'Not created. There is no some field in request data'})
    #     # # print(values)
    #     # try:
    #     #     kwargs = {keys[i]: values[i] for i in range(len(keys)) if values[i] is not None}
    #     #     # kwargs = {keys[i]: values[i] for i in range(len(keys))}
    #     #     print(kwargs)
    #     #     product = Product.objects.create(**kwargs)
    #     #     print(product)
    #     #     return Response({'created': True,
    #     #                      'message': 'Product object is successfully created',
    #     #                      'product': model_to_dict(product)})
    #     # except:
    #     #     return Response({'created': False,
    #     #                      'message': 'Not acceptable data'})
    #     new_product = Product.objects.create(
    #         image=request.data['image'],
    #         name=request.data['name'],
    #         product_slug=request.data['product_slug'],
    #         category_id=request.data['category_id'],
    #         price=request.data['price'],
    #         description=request.data['description'],
    #         quantity=request.data['quantity'],
    #         discount=request.data['discount'],
    #     )
    #     return Response({'created': True,
    #                      'message': 'Product object is successfully created',
    #                      'product': model_to_dict(new_product)})


# class CategoryAPIView(APIView):
#     def get(self, request):


# class CategoryAPIView(generics.ListAPIView):
#     queryset = Product.objects.order_by('-id')
#     serializer_class = serializers.CategorySerializer
