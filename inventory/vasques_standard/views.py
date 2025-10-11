from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .models import City, VasquesEmission


class VasquesEmissionForm(forms.ModelForm):
    class Meta:
        model = VasquesEmission
        exclude = ("city",)

    def clean_city(self):
        return City("Itajaí", 1.1)


class VasquesEmissionListView(ListView):
    model = VasquesEmission
    template_name = "vasques_list.html"


class VasquesEmissionCreateView(CreateView):
    model = VasquesEmission
    form_class = VasquesEmissionForm
    template_name = "index.html"
    success_url = reverse_lazy("vasques")

    def form_valid(self, form):
        messages.success(self.request, "Emissão adicionada com sucesso.")
        return super().form_valid(form)


class VasquesEmissionDeleteView(DeleteView):
    model = VasquesEmission
    success_url = reverse_lazy("vasques")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        pk = obj.pk
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Emissão com ID {pk} removida.")
        return response
