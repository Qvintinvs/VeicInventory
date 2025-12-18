from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from django.template.response import TemplateResponse
from django.http import HttpRequest
from django.middleware.csrf import get_token
from markupsafe import Markup

from .models import WRFStandardEmission


class FieldWrapper:
    """Wrap a Django BoundField to provide a small WTForms-like API used in templates."""
    def __init__(self, bound_field, request=None):
        self._bf = bound_field
        self._request = request

    @property
    def errors(self):
        return self._bf.errors

    def label(self, **attrs):
        return self._bf.label_tag(attrs=attrs)

    def __call__(self, **attrs):
        # Render the widget with provided attrs (e.g., class="form-control")
        return Markup(self._bf.as_widget(attrs=attrs))

    def __getattr__(self, name):
        return getattr(self._bf, name)


class WTFormsCompatibleFormWrapper:
    """Wraps a Django form to be compatible with WTForms-based Jinja2 templates."""
    def __init__(self, django_form, request=None):
        self._form = django_form
        self._request = request

    def hidden_tag(self):
        if self._request:
            csrf_token = get_token(self._request)
            html = f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">'
            return Markup(html)  # Mark as safe HTML so Jinja2 won't escape it
        return ""

    def _bound_field(self, name):
        if name in self._form.fields:
            return self._form[name]
        raise AttributeError(name)

    def __getattr__(self, name):
        try:
            bound = self._bound_field(name)
            return FieldWrapper(bound, request=self._request)
        except AttributeError:
            return getattr(self._form, name)

    def __getitem__(self, key):
        bound = self._bound_field(key)
        return FieldWrapper(bound, request=self._request)

    def __iter__(self):
        for name in self._form.fields:
            yield FieldWrapper(self._form[name], request=self._request)


class WRFStandardEmissionForm(forms.ModelForm):
    class Meta:
        model = WRFStandardEmission
        fields = "__all__"


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


def render_inventory_page(request: HttpRequest):
    # Handle POST (form submission to add vehicle)
    if request.method == "POST":
        django_form = WRFStandardEmissionForm(request.POST)
        if django_form.is_valid():
            django_form.save()
            messages.success(request, "Veículo adicionado com sucesso!")
    
    # Convert queryset to lightweight objects matching the original Flask template expectations.
    from types import SimpleNamespace

    qs = WRFStandardEmission.objects.all()
    view_items = []
    for v in qs:
        # subcategory.display from choices, fallback to raw value
        try:
            subcat_display = v.get_subcategory_display()
        except Exception:
            subcat_display = str(v.subcategory)

        subcat_obj = SimpleNamespace(name=subcat_display)

        item = SimpleNamespace(
            id=v.pk,
            year=getattr(v, "year", ""),
            fuel=v.fuel,
            subcategory=subcat_obj,
            mileage=v.mileage,
            fraction=v.fraction,
            note=v.note,
        )
        view_items.append(item)

    django_form = WRFStandardEmissionForm()
    form = WTFormsCompatibleFormWrapper(django_form, request)
    context = {"emission_data": view_items, "form": form}
    return TemplateResponse(request, "index.html", context, using="jinja2")


def delete_vehicle_emission(request: HttpRequest, emission_id: int):
    """Delete a vehicle emission by ID (accepts both GET and POST)."""
    try:
        vehicle = WRFStandardEmission.objects.get(pk=emission_id)
        vehicle.delete()
        messages.success(request, f"Veículo com ID {emission_id} removido com sucesso.")
    except WRFStandardEmission.DoesNotExist:
        messages.error(request, f"Veículo com ID {emission_id} não encontrado.")
    
    # Redirect back to inventory page
    from django.shortcuts import redirect
    return redirect("home")


def schedule_emission_round(request: HttpRequest, emission_id: int):
    """Schedule an emission round for a vehicle (placeholder for future implementation)."""
    # TODO: Implement emission round scheduling logic
    messages.info(request, f"Função de agendamento em desenvolvimento para o veículo {emission_id}.")
    from django.shortcuts import redirect
    return redirect("home")


def visualize(request: HttpRequest):
    """Render the visualization/plot template (render_plot.html)."""
    context = {}
    return TemplateResponse(request, "render_plot.html", context, using="jinja2")
