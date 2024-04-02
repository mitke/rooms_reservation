from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('administracija/', admin.site.urls),
    #path('bookingRooms', include('bookingRooms/urls')),
    path('', include('booking.urls')),
]
