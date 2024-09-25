from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Resourse, Booking, BookingQueue
from .serializers import BookingSerializer, ResourceSerializer
from .tasks import notify_user_about_free_slot
from django.utils import timezone


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resourse.objects.all()
    serializer_class = ResourceSerializer
    

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    
    def create(self, request, *args, **kwargs):
        
        resource_id = request.data.get('resource')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        resource = Resourse.objects.get(id=resource_id)
        
        conflicting_bookings = Booking.objects.filter(
            resource = resource,
            start_time__lt = end_time,
            end_time__lt = start_time,
            status = 'active',
        )
        
        if conflicting_bookings.count() < resource.max_slots:
            return super().create(request, *args, **kwargs)
        
        else:
            booking = Booking.objects.create(
                user = request.user,
                resource = resource,
                start_time = start_time,
                end_time = end_time,
                status = 'queue'
            )
            
            queue_position = BookingQueue.objects.filter(booking__resource = resource).count() + 1
            BookingQueue.objects.create(booking = booking, position = queue_position)
            return Response({"detail": "Added to queue", "queue_position": queue_position})
        
        
    def destroy(self, request, *args, **kwargs):
        
        booking = self.get_object()
        resource = booking.resource
        user_email = booking.user.email
        booking.delete()
        
        next_in_queue = BookingQueue.objects.filter(booking__resource = resource).order_by('position').first()
        if next_in_queue:
            next_booking = next_in_queue.booking
            next_booking.status = 'active'
            next_booking.save()
            next_in_queue.delete()
            notify_user_about_free_slot.delay(next_booking.user.email, resource.name)
            
            return Resourse({'detail': f"Booking transferred ot {next_booking.user.username}"})
        
        return Resourse({'detail': "Booking cancelled"})
    
    