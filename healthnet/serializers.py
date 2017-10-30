from django.contrib.auth.models import User, Group
from rest_framework import serializers
from healthnet.models import Score


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name', 'password', 'is_superuser')
        write_only_fields = ('password',)

    def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'score','owner_name','game', 'updated')
