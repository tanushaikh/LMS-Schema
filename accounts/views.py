from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from accounts.serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        print('Tanu',request.data)
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            
            return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        print('username',username)
        print('password',password)
        print('user',user)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)