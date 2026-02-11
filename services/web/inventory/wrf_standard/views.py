from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .models import WRFStandardEmission


class WRFStandardEmissionForm(forms.ModelForm):
    class Meta:
        model = WRFStandardEmission
        include = "__all__"


class WRFStandardEmissionListView(ListView):
    model = WRFStandardEmission
    template_name = "wrf_standard_list.html"


class WRFStandardEmissionCreateView(CreateView):
    model = WRFStandardEmission
    form_class = WRFStandardEmissionForm
    template_name = "index.html"
    success_url = reverse_lazy("wrf_standard")

    def form_valid(self, form):
        messages.success(self.request, "Emissão adicionada com sucesso.")
        return super().form_valid(form)


class WRFStandardEmissionDeleteView(DeleteView):
    model = WRFStandardEmission
    success_url = reverse_lazy("wrf_standard")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        pk = obj.pk
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Emissão com ID {pk} removida.")
        return response
