from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status
from .serializers import UserRegisterSerializer, UserAuthSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


@api_view(['POST'])
def register_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user= User.objects.create_user(username=username,
                                   password=password,
                                   is_active=True)

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})

class AuthApiView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user= authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={'User credentials invalid.'})
