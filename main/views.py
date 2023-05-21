from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from main.models import Product, Cart, Order
from main.permissions import IsAuthOrNotAdminUser
from main.serializers import UserLoginSerializer, ProductSerializer, ProductCartSerializer, OrderSerializer, \
    UserRegisterSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'data': {"user_token": token.key}}, status=status.HTTP_200_OK)
        return Response({'error': {"code": 401, 'message': "Authentication failed"}},
                        status=status.HTTP_401_UNAUTHORIZED)
    return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_signup_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'data': {"user_token": token.key}}, status=status.HTTP_201_CREATED)
    return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_logout_view(request):
    request.user.auth_token.delete()
    return Response({'data': {'message': "logout"}}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def product_list_view(request):
    serializer = ProductSerializer(Product.objects.all(), many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def create_product_for_admin(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data': {"id": serializer.data['id'], 'message': "Product added"}},
                        status=status.HTTP_201_CREATED)
    return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['DELETE', 'PATCH'])
@permission_classes((IsAdminUser,))
def edit_or_delete_product_for_admin(request, **kwargs):
    product_id = kwargs.get('product_id', None)

    try:
        product = Product.objects.get(pk=product_id)
    except:
        return Response({"error": {"code": 404, "message": "Not Found"}},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response({"data": {'message': "Item removed"}}, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
@permission_classes((IsAuthOrNotAdminUser,))
def cart_list(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    if not products.exists():
        return Response({'error': {"code": 403, "message": "Cart is empty"}},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = ProductCartSerializer(products, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthOrNotAdminUser,))
def add_product_to_cart_or_delete(request, **kwargs):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product_id = kwargs.get('product_id', None)

    try:
        product = Product.objects.get(pk=product_id)
    except:
        return Response({"error": {"code": 404, "message": "Not Found"}},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        cart.products.add(product)
        return Response({"data": {'message': "Product add to cart"}}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        cart.products.remove(product_id)
        return Response({"data": {'message': "Product remove from cart"}}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthOrNotAdminUser,))
def get_post_order_view(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)

        if not cart.products.exists():
            return Response({'error': {'code': 422, 'message': 'Cart is empty'}},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        order_price = sum([product.price for product in cart.products.all()])
        order = Order.objects.create(
            user=request.user,
            order_price=order_price
        )
        order.products.set(cart.products.all())
        cart.delete()

        return Response({'data': 'order is processed'}, status=status.HTTP_201_CREATED)