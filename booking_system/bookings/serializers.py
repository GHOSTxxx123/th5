from rest_framework import serializers 
from .models import Booking, Resourse


class ResourceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Resourse
        fields = '__all__'
        
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
        
        