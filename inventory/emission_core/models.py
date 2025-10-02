from django.db import models


class EmissionManager(models.Manager):
    def list_emissions(self, limit=5):
        return self.all()[:limit]

    def read_emission_by_id(self, emission_id: int):
        return self.filter(id=emission_id).first()

    def delete_data_by_id(self, emission_id: int):
        return self.filter(id=emission_id).delete()
