from rest_framework.permissions import BasePermission
from organization_app.models import OrganizationResponsible


class IsResponsible(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        organization = request.data.get('organization')

        return OrganizationResponsible.objects.filter(organization=organization, user=request.user).exists()
