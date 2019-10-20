from django.forms import ModelForm
from network.models import add_userinfo
from django import forms


class add_userinfo_form(ModelForm):
    class Meta:
        model = add_userinfo
        fields = ['long', 'lat', 'local_address', 'phone']
