from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
import jwt

from .authentication import TokenAuthentication
from .serializers import UserCreationSerializer
from .models import User, Token

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

SECRET_KEY_DEMO = 'qwertyuiopsdfghjklzxcvbnm'

class test(APIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [AdminOrTeacherOnly,]

    def get(self, request, *args,**kwargs):
        abc = {"hello":"hello world", "hello2":"Hello World 2"}
        publish(method="test_data", body=abc)
        return Response("Success", status=HTTP_200_OK)

class UserCreateView(APIView):
    ''' Params ("email", "password", "password2")'''

    permission_classes = [AllowAny]
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={
                    "Status":HTTP_200_OK,
                    "Message":"User Created Successfully",
                    "Result":serializer.data}, 
                status=HTTP_200_OK
            )
        return Response(
            data={
                "Status":HTTP_400_BAD_REQUEST,
                "Result":serializer.errors}, 
            status=HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args,**kwargs):
        if not request.data['email'] or not request.data['password']:
            return Response(
                data={
                    "Status":HTTP_400_BAD_REQUEST,
                    "Message":"Email and Password is must to login."},
                status=HTTP_400_BAD_REQUEST
            )
        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)
        if user is None:
            return Response(
                data={
                    "Status":HTTP_400_BAD_REQUEST,
                    "Message":"Email or Password is Incorrect."},
                status=HTTP_400_BAD_REQUEST
            )
        payload = {
            "username":user.username,
            "email":user.email,
            "datetime": str(datetime.now())}
        jwt_token = jwt.encode(payload, SECRET_KEY_DEMO, algorithm='HS256')
        try:
            d_token = Token.objects.get(user=user)
            d_token.token = jwt_token
            expire_time = datetime.today() + timedelta(hours=24)
            d_token.expire = expire_time
            d_token.save()
        except:
            expire_time = datetime.today() + timedelta(hours=24)
            d_token = Token.objects.create(user=user, token=jwt_token, expire=expire_time)
        login_data = {"email":user.email, "token":str(jwt_token)}
        return Response(
            data={
                "Status":HTTP_200_OK,
                "Message":"Login Successfully.",
                "Result":{"Token":jwt_token}}, 
            status=HTTP_200_OK
        )