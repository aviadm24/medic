from import_export import resources
from .models import Medication


class MedicationResource(resources.ModelResource):
    class Meta:
        model = Medication