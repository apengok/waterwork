python manage.py dumpdata accounts.MyRoles --indent 2 > role.json
python manage.py loaddata entm/fixtures/organization_init.json