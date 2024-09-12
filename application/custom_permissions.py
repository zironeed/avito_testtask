from rest_framework.permissions import BasePermission
from organization_app.models import OrganizationResponsible


class IsResponsible(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        organization = request.data.get('organization')

        return OrganizationResponsible.objects.filter(organization=organization, user=request.user).exists()


class IsResponsibleOrAuthor(BasePermission):

    def has_permission(self, request, view):
        bid = view.get_object()
        is_author = bid.creator == request.user
        is_responsible = OrganizationResponsible.objects.filter(organization=bid.organization,
                                                                user=request.user).exists()

        return is_author or is_responsible


class IsTenderResponsible(BasePermission):

    def has_permission(self, request, view):
        user_tenders = self.request.user.tenders.all()
        bid_tender = view.get_object().tender

        return bid_tender in user_tenders
