from django import forms, views
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import City, VasquesEmission


class VasquesEmissionForm(forms.ModelForm):
    class Meta:
        model = VasquesEmission
        exclude = ("city",)

    def clean_city(self):
        return City("Itajaí", 1.1)


class VasquesEmissionView(views.View):
    template_name = "index.html"

    def get(self, request):
        emissions = VasquesEmission.objects.all()

        form = VasquesEmissionForm()

        return render(
            request, self.template_name, {"emission_data": emissions, "form": form}
        )

    def post(self, request):
        form = VasquesEmissionForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Emissão adicionada com sucesso.")

        return redirect("vasques_inventory")

    def delete(self, request, pk):
        emission = get_object_or_404(VasquesEmission, pk=pk)
        emission.delete()

        messages.success(request, f"Emissão com ID {pk} removida.")

        return redirect("vasques_inventory")
