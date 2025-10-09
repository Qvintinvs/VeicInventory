from django import forms
from django.shortcuts import render

from .models import VasquesEmission


class VasquesEmissionForm(forms.ModelForm):
    class Meta:
        model = VasquesEmission
        exclude = ("city",)
