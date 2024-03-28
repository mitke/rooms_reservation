from django.contrib import admin
from .models import Rooms, Bookings
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class RoomsAdmin(admin.ModelAdmin):
  list_display = ('name', 'capacity', 'projector')


class BookingsAdmin(admin.ModelAdmin):
  list_display = ('room', 'user', 'start_time', 'end_time', 'organizer_name', 'purpose', 'expected_participants', 'napomena')


admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Bookings, BookingsAdmin)


class UserProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete = False
  verbose_name_plural = 'User Profile'
  
class CustomUserAdmin(UserAdmin):
  inlines = (UserProfileInline, )

admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)


