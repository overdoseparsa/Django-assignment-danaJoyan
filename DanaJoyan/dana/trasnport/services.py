from django.db import transaction

from .models import Transport , Admin


def create_transport(validated_data, admin_user: Admin):
 
    name = validated_data.get('name')
    bus = validated_data.get('bus')
    seats = validated_data.get('seat', []) 
    
    if bus.author != admin_user:
        raise ValueError("Bus author must be the same as transport author")
    

    transport = Transport.objects.create(
        name=name,
        bus=bus,
        author=admin_user
    )
    
    for seat in seats:
        if seat.bus != bus:
            transport.delete() 
            raise ValueError(f"Seat {seat.seat_number} bus must be the same as transport bus")
        
        if seat.author != admin_user:
            transport.delete()
            raise ValueError(f"Seat {seat.seat_number} author must be the same as transport author")
        
        transport.seat.add(seat)
    
    return transport