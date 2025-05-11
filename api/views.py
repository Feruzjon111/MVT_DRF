import random
import re
import uuid
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from .methods.helper import send_code
from .models import OTP
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from KirimChiqim.models import Transaction
from .serializers import TransactionSerializer


class ListCreateAPI(APIView):

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailAPI(APIView):

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# byyog'i register qismi

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Muvaffaqiyatli kirildi!",
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Muvaffaqiyatli chiqildi"}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ma'lumotlar to'liq yangilandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ma'lumotlar qisman yangilandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Akkount o'chirildi"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user
        old = request.data.get("old")
        new = request.data.get("new")
        confirm = request.data.get("confirm")

        if not user.check_password(old):
            return Response({"error": "Hozirgi parolni to'g'ri kiriting."}, status=status.HTTP_400_BAD_REQUEST)

        if new != confirm:
            return Response({"error": "New password va confirm password mos kelmadi."}, status=status.HTTP_400_BAD_REQUEST)

        if old == new:
            return Response({"error": "hozirgi password va yangi password bir xil bolishi mumkin emas."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new)
        user.save()

        return Response({"success": "Password muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_200_OK)

EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')


class Email_or_Phone(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        phone = data.get('phone')

        if not email and not phone:
            return Response({'error': "Kamida telefon yoki email kiriting"}, status=400)

        is_email = isinstance(email, str) and EMAIL_REGEX.match(email)
        is_phone = isinstance(phone, str) and phone.isdigit() and len(phone) == 12 and phone.startswith("998")

        if email and not is_email:
            return Response({'error': "Email formati noto‘g‘ri"}, status=400)

        if phone and not is_phone:
            return Response({'error': "Telefon raqami noto‘g‘ri"}, status=400)

        code = str(random.randint(1000, 9999))
        key = str(uuid.uuid4()) + code

        if is_email:
            print(f"EMAILga yuborilgan kod: {code}")
            send_code(email, code)
        if is_phone:
            print(f"PHONEga yuborilgan kod: {code}")
            send_code(phone, code)

        OTP.objects.create(phone=phone or '', key=key)
        return Response({
            'otp': code,
            'token': key
        })


class Auth(APIView):
    def post(self, request):
        data = request.data
        code = data.get('code')
        key = data.get('key')

        if not code or not key:
            return Response({
                "error": "To‘liq ma’lumot kiriting (code va key)"
            }, status=400)

        otp = OTP.objects.filter(key=key).first()

        if not otp:
            return Response({"error": "Noto‘g‘ri key"}, status=400)

        if otp.is_expire:
            return Response({"error": "Kod muddati tugagan"}, status=400)

        if otp.tried >= 3:
            otp.is_expire = True
            otp.save()
            return Response({"error": "Juda ko‘p urinish"}, status=400)

        if not str(code) in otp.key:
            otp.tried += 1
            otp.save()
            return Response({"error": "Kod noto‘g‘ri"}, status=400)

        otp.is_conf = True
        otp.save()
        return Response({"message": "Kod tasdiqlandi!"}, status=200)

