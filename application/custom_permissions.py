from rest_framework.permissions import BasePermission
from .organization_app.models import OrganizationResponsible


class IsResponsible(BasePermission):

    def has_permission(self, request, view):
        try:
            creator = request.user.id

            if request.method in ['GET', 'PATCH', 'PUT']:
                organization_responsible = OrganizationResponsible.objects.filter(user=request.user).first()

                if organization_responsible:
                    organization_id = organization_responsible.organization.id
                    return OrganizationResponsible.objects.filter(organization__id=organization_id,
                                                                  user__id=creator).exists()
                return False

            organization_id = request.data.get('organization')

            return OrganizationResponsible.objects.filter(organization__id=organization_id, user__id=creator).exists()
        except Exception as e:
            print(f"Error in permission: {e}")
            return False


class IsResponsibleOrAuthor(BasePermission):

    def has_permission(self, request, view):
        bid = view.get_object()
        if request.method in ['POST', 'PATCH', 'PUT']:
            organization = request.data.get('organization')
            if organization:
                return all(OrganizationResponsible.objects.filter(
                    organization=organization,
                    user=request.user
                ).exists(), (bid.creator == request.user))
            return bid.creator == request.user

        is_author = bid.creator == request.user
        is_responsible = OrganizationResponsible.objects.filter(organization=bid.organization,
                                                                user=request.user).exists()

        return is_author or is_responsible


class IsTenderResponsible(BasePermission):

    def has_permission(self, request, view):
        user_tenders = request.user.tenders.all()
        bid_tender = view.get_object().tender

        return bid_tender in user_tenders
