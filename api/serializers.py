from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from auth_app.models import CustomUser

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        if not password:
            raise serializers.ValidationError("Parol kiritilishi shart!")

        if not email and not phone:
            raise serializers.ValidationError("Email yoki telefon raqamni kiriting!")

        user = None
        if email:
            user = authenticate(username=email, password=password)
        elif phone:
            try:
                user_obj = User.objects.get(phone=phone)
                user = authenticate(username=user_obj.email, password=password)
            except User.DoesNotExist:
                raise serializers.ValidationError("Bunday foydalanuvchi mavjud emas!")

        if user is None:
            raise serializers.ValidationError("Kirish ma'lumotlari noto‘g‘ri!")

        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi faol emas!")

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name']

from rest_framework import serializers
from KirimChiqim.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
