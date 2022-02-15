from rest_framework import serializers
from shop.models import TeleVision, Phones, PersonalComputers


# Making serializers for all our product 'Modells'.
class PhonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phones
        fields = ("id", "brand", "model", "description", "price", "available",
                  "quantity")


class TeleVisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeleVision
        fields = ("id", "brand", "model", "description", "price", "available",
                  "quantity")


class PersonalComputersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalComputers
        fields = ("id", "brand", "model", "description", "price", "available",
                  "quantity")
