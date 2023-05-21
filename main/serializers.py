from django.contrib.auth import authenticate
from rest_framework import serializers

from main.models import User, Product, Order


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            user = authenticate(self.context.get('request'), email=email, password=password)
            attrs['user'] = user
            return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fio', 'password')

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            fio=self.validated_data['fio'],
            username=self.validated_data['fio'],
        )
        if self.validated_data['password']:
            user.set_password(self.validated_data['password'])
            user.save()
            return user
        return serializers.ValidationError({"password": "Password not valid"})


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')

    class Meta:
        model = Product
        fields = ['id', 'product_id', 'name', 'description', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'products', 'order_price']
