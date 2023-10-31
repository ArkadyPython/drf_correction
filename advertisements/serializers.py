from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )
        read_only_fields = ['creator',]

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        if self.context["request"].method == 'POST':
            if Advertisement.objects.filter(creator_id = self.context["request"].user, status='OPEN').count() <= 10:
                return data
            else:
                raise serializers.ValidationError('Пользователь имеет слишком много открытых объявлений')
        if self.context["request"].method == 'PATCH' \
                and Advertisement.objects.filter(creator_id = self.context["request"].user, status='OPEN').count() >= 1:
            if Advertisement.objects.filter(creator_id = self.context["request"].user, status='OPEN').count() <= 10:
                return data
            else:
                raise serializers.ValidationError('Пользователь имеет слишком много открытых объявлений')
