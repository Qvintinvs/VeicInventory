from django import forms, views
from django.shortcuts import render

from .models import City, VasquesEmission


class VasquesEmissionForm(forms.ModelForm):
    class Meta:
        model = VasquesEmission
        exclude = ("city",)

    def clean_city(self):
        return City("Itajaí", 1.1)


class VasquesEmissionView(views.View):
    pass
