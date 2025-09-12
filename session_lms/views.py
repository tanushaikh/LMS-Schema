from rest_framework import viewsets
from .models import Session
from .serializers import SessionSerializer
from accounts.models import User

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    class SessionViewSet(viewsets.ModelViewSet):
        queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # agar authentication use nahi kar rahe ho to test ke liye
            default_user = User.objects.first()  # pehla user assign ho jayega
            serializer.save(user=default_user)
