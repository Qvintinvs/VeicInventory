from models.cnh_subcategory import CNHSubcategory
from wtforms import SelectField
from wtforms.validators import AnyOf, DataRequired


class SubcategoryField(SelectField):
    __validators = (
        DataRequired(),
        AnyOf(tuple(subcategory.name for subcategory in CNHSubcategory)),
    )

    __label = "Subcategoria:"

    __choices = (
        ("", "Selecione a subcategoria de CNH..."),
        ("A", "A - Motos, motonetas e triciclos"),
        ("B", "B - Carros de passeio, utilitário/SUV, minivan, picape"),
        ("C", "C - Caminhões, caminhonetes, vans de carga"),
        ("D", "D - Ônibus, microônibus, vans de passageiros"),
        ("E", "E - Veículos pesados"),
    )

    def __init__(self, **kwargs):
        super().__init__(
            label=self.__label,
            choices=self.__choices,
            validators=self.__validators,
            **kwargs,
        )

    @property
    def cnh_subcategory(self):
        form_value: str | None = self.data

        matches_in_the_cnh_subcategories = (
            subcategory.value
            for subcategory in CNHSubcategory
            if subcategory.name == form_value
        )

        subcategory_of_the_value = next(matches_in_the_cnh_subcategories, None)

        if subcategory_of_the_value is None:
            raise ValueError(f"Invalid value for CNHSubcategory: {form_value}")

        return subcategory_of_the_value
