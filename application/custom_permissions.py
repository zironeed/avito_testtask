from rest_framework.permissions import BasePermission
from .organization_app.models import OrganizationResponsible


class IsResponsible(BasePermission):

    def has_permission(self, request, view):
        try:
            creator = request.user

            if request.method == 'GET':
                organization_responsible = OrganizationResponsible.objects.filter(user=request.user).first()

                if organization_responsible:
                    organization_id = organization_responsible.organization
                    return OrganizationResponsible.objects.filter(organization__id=organization_id,
                                                                  user__id=creator).exists()
                else:
                    return False

            organization_id = request.data.get('organization')

            return OrganizationResponsible.objects.filter(organization__id=organization_id, user__id=creator).exists()
        except Exception as e:
            print(f"Error in permission: {e}")
            return False


class IsResponsibleOrAuthor(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return OrganizationResponsible.objects.filter(
                organization=request.data.get('organization'),
                user=request.user
            ).exists()

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
