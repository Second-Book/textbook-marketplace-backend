from rest_framework import serializers

from .models import Textbook, User, Order 
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.conf import settings


class AbsoluteVersatileImageFieldSerializer(VersatileImageFieldSerializer):
    def to_representation(self, value):
        data = super().to_representation(value)
        if isinstance(data, dict):
            return {
                key: f"{settings.MEDIA_HOST}{url}" if url.startswith("/media/") else url
                for key, url in data.items()
            }
        return data


class TextbookSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')
    image = AbsoluteVersatileImageFieldSerializer(sizes='marketplace')


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
        model = User
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')
    textbook = serializers.ReadOnlyField(source='textbook.title')

    class Meta:
        model = Order
        fields = '__all__'

