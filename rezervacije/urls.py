from django.contrib import admin
from django.urls import path, include

urlpatterns = [
        path('administracija/', admin.site.urls), ### admin:T1rs0va.
    #path('bookingRooms', include('bookingRooms/urls')),
    path('', include('booking.urls')),
]
