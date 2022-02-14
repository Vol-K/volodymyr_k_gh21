from rest_framework import viewsets
from rest_framework import permissions


from .models import TeleVision, Phones, PersonalComputers
from .serializers import PhonesSerializer, TeleVisionSerializer, PersonalComputersSerializer


# Creating views for the 'serializers' for all product models.
class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phones.objects.all()
    serializer_class = PhonesSerializer
    permission_class = [permissions.IsAuthenticated]


class TeleVisionViewSet(viewsets.ModelViewSet):
    queryset = TeleVision.objects.all()
    serializer_class = TeleVisionSerializer
    permission_class = [permissions.IsAuthenticated]


class PersonalComputersViewSet(viewsets.ModelViewSet):
    queryset = PersonalComputers.objects.all()
    serializer_class = PersonalComputersSerializer
    permission_class = [permissions.IsAuthenticated]
