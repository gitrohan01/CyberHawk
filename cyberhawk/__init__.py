import django
from django.db.models import CharField, TextField

# Fix MySQL index length issue
CharField.register_lookup(django.db.models.lookups.IExact, lookup_name='iexact')
TextField.register_lookup(django.db.models.lookups.IExact, lookup_name='iexact')
