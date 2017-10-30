from django.contrib.auth.models import User, Group
from rest_framework import serializers
from healthnet.models import Score
from django.forms.models import model_to_dict

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
    owner = serializers.SerializerMethodField('get_sr_price_func')

    def get_sr_price_func(self, obj):
        return model_to_dict(self.context['request'].user.account)
    class Meta:
        model = Score
        fields = ('score','game','owner','id')
        write_only_fields = ('score','game','owner')

    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['owner'] = self.context['request'].user.account
            return validated_data
