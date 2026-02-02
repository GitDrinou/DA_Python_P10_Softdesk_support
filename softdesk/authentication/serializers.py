from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for our custom user model """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'password',
        ]
        extra_kwargs = {
            "age": {"required": True},
        }

    def create(self, validated_data):
        """ Create and return a new user """
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared'],
        )

        return user

    def validate_age(self, value):
        """ Validate the user age to be more than 15 years old """
        if value < 15:
            raise serializers.ValidationError(
                "You must be at least 15 years old to create an account"
            )

        return value
