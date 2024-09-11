from rest_framework import serializers
from .models import Organization, OrganizationResponsible


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationResponsibleSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationResponsible
        fields = '__all__'
