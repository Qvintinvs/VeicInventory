from django.test import TestCase
from django.urls import reverse

from .models import WRFStandardEmission


class WRFStandardViewsTest(TestCase):
    def test_list_page_loads(self):
        response = self.client.get(reverse("wrf_standard"))
        self.assertEqual(response.status_code, 200)
        # button should open the add-emission modal rather than navigate
        self.assertContains(response, "data-bs-target=\"#addModal\"")
        # JavaScript uses fetch() to load the add form
        self.assertContains(response, "fetch(window.location.origin")
        self.assertContains(response, "/wrf-standard/add/?modal=1")
        # table headers and badges
        self.assertContains(response, "Combustível")
        self.assertContains(response, "Categoria")
        self.assertContains(response, "Nota")
        self.assertContains(response, "Autonomia")
        self.assertContains(response, "Fração")
        self.assertContains(response, "Status")
        self.assertContains(response, "badge-transition")
        # Edit button should be available for each row
        # create a sample object to render
        WRFStandardEmission.objects.create(
            fuel="Gasoline",
            fraction=1.0,
            mileage=10.0,
            note="x",
            subcategory="B",
        )
        response = self.client.get(reverse("wrf_standard"))
        self.assertContains(response, "wrf-standard/edit/")
        # should expose a data-edit-url for the JS handler
        self.assertContains(response, "data-edit-url")
        # delete button now comes from a POST form
        self.assertContains(response, "class=\"delete-form\"")

    def test_add_modal_uses_bare_template(self):
        url = reverse("wrf_standard_add") + "?modal=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # should render form but not the page header
        self.assertContains(response, "Adicionar emissão WRF")
        self.assertNotContains(response, "Inventário Veicular")
        # the modal form still includes a valid action attribute
        self.assertContains(response, "action=\"/wrf-standard/add/\"")
        # check that individual fields are present with correct labels
        self.assertContains(response, "Nota do veículo")
        self.assertContains(response, "Combustível")
        self.assertContains(response, "Subcategoria")
        self.assertContains(response, "Autonomia do Veículo")
        self.assertContains(response, "Fração do Veículo na frota")

    def test_add_page_layout(self):
        response = self.client.get(reverse("wrf_standard_add"))
        self.assertEqual(response.status_code, 200)
        # layout should include bootstrap row/col structure
        self.assertContains(response, "col-md-6")
        self.assertContains(response, "form-control")
        # dropdown labels should be translated
        self.assertContains(response, "Gasolina")
        self.assertContains(response, "Álcool")
        self.assertContains(response, "B - Carros de passeio")
        # placeholders should be visible on inputs
        self.assertContains(response, "placeholder=\"Ex: 12.5 (km/L)\"")
        self.assertContains(response, "placeholder=\"Ex: 15 (%)\"")
        # verify the form action is set correctly
        self.assertContains(response, "action=\"/wrf-standard/add/\"")

    def test_update_page_and_modal(self):
        # create an object to edit
        obj = WRFStandardEmission.objects.create(
            fuel="Gasoline",
            fraction=1.0,
            mileage=10.0,
            note="foo",
            subcategory="B",
        )
        url = reverse("wrf_standard_edit", args=[obj.pk])

        # normal GET should show "Editar" heading and pre-populated notes
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar emissão WRF")
        self.assertContains(response, "foo")
        # form action should default to this url
        self.assertContains(response, f"action=\"{url}\"")

        # modal variant should use bare template but still say "Editar"
        response = self.client.get(url + "?modal=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar emissão WRF")
        self.assertNotContains(response, "Inventário Veicular")
        # the modal form must carry an action pointing at the edit URL
        self.assertContains(response, f"action=\"{url}\"")

        # posting updated data should redirect back to list
        data = {
            "fuel": obj.fuel,
            "fraction": obj.fraction,
            "mileage": obj.mileage,
            "note": "updated",
            "subcategory": obj.subcategory,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("wrf_standard"))
        obj.refresh_from_db()
        self.assertEqual(obj.note, "updated")

        # also exercise deletion: create a second object and POST a delete
        obj2 = WRFStandardEmission.objects.create(
            fuel="Gasoline",
            fraction=1.0,
            mileage=10.0,
            note="to be removed",
            subcategory="B",
        )
        del_url = reverse("wrf_standard_delete", args=[obj2.pk])
        # GET should not render a confirmation page; just redirect
        response = self.client.get(del_url)
        self.assertRedirects(response, reverse("wrf_standard"))
        # actual deletion happens on POST
        response = self.client.post(del_url)
        self.assertRedirects(response, reverse("wrf_standard"))
        self.assertFalse(WRFStandardEmission.objects.filter(pk=obj2.pk).exists())

        # repeating the POST with ?modal=1 should behave identically
        response = self.client.post(url + "?modal=1", data)
        self.assertRedirects(response, reverse("wrf_standard"))
        obj.refresh_from_db()
        self.assertEqual(obj.note, "updated")

    def test_visualize_modal_url(self):
        response = self.client.get(reverse("wrf_standard_visualize"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Este recurso ainda não foi implementado.")
