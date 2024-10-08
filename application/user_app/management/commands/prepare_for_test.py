from django.core.management import BaseCommand, call_command
from application.user_app.models import Employee
from application.organization_app.models import Organization, OrganizationResponsible


class Command(BaseCommand):
    help = 'Prepare for test'

    def handle(self, *args, **options):
        call_command('makemigrations', verbosity=0)
        call_command('migrate', verbosity=0)

        try:
            call_command('createsuperuser', username='admin', email='', interactive=False)
            user = Employee.objects.get(username='admin')
            user.set_password('admin')
            user.save()
        except Exception:
            print('User already exists')

        try:
            org_1 = Organization.objects.create(
                name='Alphabet',
                description='organization 1',
                type=Organization.OrganizationType.LLC
            )
            org_1.save()
        except Exception:
            print('Organization already exists')
        try:
            org_2 = Organization.objects.create(
                name='Apple',
                description='organization 2',
                type=Organization.OrganizationType.IE
            )
            org_2.save()
        except Exception:
            print('Organization already exists')

        try:
            emp_1 = Employee.objects.create(
                username='organization_user',
                first_name='User',
                last_name='One'
            )
            emp_1.set_password('12345')
            emp_1.save()
        except Exception:
            print('User already exists')
        try:
            emp_2 = Employee.objects.create(
                username='default_user',
                first_name='User',
                last_name='Two'
            )
            emp_2.set_password('12345')
            emp_2.save()
        except Exception:
            print('User already exists')

        try:
            resp = OrganizationResponsible.objects.create(
                organization=org_1,
                user=emp_1
            )
            resp.save()
        except Exception:
            print('Responsible already exists')

        print("""
        2 организации - Alphabet и Apple
        Обычный пользователь - default_user, password - 12345
        Пользователь с организацией - organization_user, password - 12345
        Администратор - admin, password - admin
        
        Хорошего вам дня :)
        """)
