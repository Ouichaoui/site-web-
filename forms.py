
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProductForm(forms.ModelForm):
    class Meta :
        model = Product
        fields = '__all__'
        exclude = ('by',)

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = '__all__'
        exclude = ('created_by','created_at','produit',)