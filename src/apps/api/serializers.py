from rest_framework import serializers

from apps.data_providers.models import LastFMAccount
from apps.music.models import Track


class LastFMAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastFMAccount
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

