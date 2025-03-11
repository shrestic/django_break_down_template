from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserRegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)