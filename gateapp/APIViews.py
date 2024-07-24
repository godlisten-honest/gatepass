# myapp/views.py
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# from django.contrib.auth.models import User
from .models import CustomUser as User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            # userData = User.objects.all()
            return Response({
                'refresh': str(refresh),
                'token': str(refresh.access_token),
                'user': user_data
            })
        else:
            return Response(
                {
                    'message': 'Incorrect username or password',
                    'code': 102,
                 }, 
                status=status.HTTP_401_UNAUTHORIZED)