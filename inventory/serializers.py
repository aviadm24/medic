from rest_framework import serializers
from .models import Medication, Order, Item, Formation, Categorical_dose, Type, Kind_name


class InventorySerializer(serializers.ModelSerializer):
    formation = serializers.ReadOnlyField(source='formation.name')
    categorical_dose = serializers.ReadOnlyField(source='categorical_dose.name')
    m_type = serializers.ReadOnlyField(source='m_type.name')
    company = serializers.ReadOnlyField(source='company.name')
    manufacturer = serializers.ReadOnlyField(source='manufacturer.name')

    class Meta:
        model = Medication
        fields = ('formation',
        'categorical_dose',
        'dose',
        'categorical_dose',
        'm_type',
        'company',
        'manufacturer',
        'kind_name',
        'pharma_code',
        'page_num',
        'price',
        'amount',
        'date_added',
        'comments')