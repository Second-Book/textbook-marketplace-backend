from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Textbook, Order
from versatileimagefield.serializers import VersatileImageFieldSerializer


class TextbookSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')
    image = VersatileImageFieldSerializer(
        sizes='marketplace',
    )

    class Meta:
        model = Textbook
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        seller = request.user
        textbook = Textbook.objects.create(seller=seller, **validated_data)
        return textbook


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')
    textbook = serializers.ReadOnlyField(source='textbook.title')

    class Meta:
        model = Order
        fields = '__all__'
