from django import forms
from .models import Bookings, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput, TextInput

class BookingForm(forms.ModelForm):
  class Meta:
    model = Bookings
    fields = ['start_time', 'end_time', 'organizer_name', 'purpose',
               'expected_participants', 'napomena']
    widgets = {
      'start_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
      'end_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
      'organizer_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Organizator'}),
      'purpose': TextInput(attrs={'class': 'form-control', 'placeholder': 'Svrha'}),
      'expected_participants': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Očekivani broj učesnika (arapskim ciframa)'}),
      #'needs_projector': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
      'napomena': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Napomena'}),
    }
    labels = {
      'start_time': 'Početak termina',
      'end_time': 'Kraj termina',
      'organizer_name': 'Organizator',
      'purpose': 'Svrha',
      'expected_participants': 'Očekivani broj učesnika',
      'napomena': '',
    }


class RegistrationForm(UserCreationForm):
  telephone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Broj telefona'}))
  medical_title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicinska titula'}))

  class Meta:
    model = User
    fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'odaberi korisničko ime'}),
      'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
      'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password2'}),
      'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ime'}),
      'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prezime'}),
      'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    }
    labels = {
      'password2': 'Potvrda passworda',
    }

  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['telephone_number'].label = 'Broj telefona'
    self.fields['medical_title'].label = 'Medicinska titula'

  def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user_profile = UserProfile(
      user=user,
      telephone_number=self.cleaned_data['telephone_number'],
      medical_title=self.cleaned_data['medical_title']
    )
    if commit:
      user.save()
      user_profile.save()
    return user



