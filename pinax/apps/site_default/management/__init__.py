"""
Update the default site domain name and display name
"""

from django.db.models import signals
from django.contrib.sites.models import Site
from django.contrib.sites import models as site_app

def update_default_site(app, created_models, verbosity, **kwargs):
    if Site in created_models:
        msg = "\nWould you like to change the default site domain name? (yes/no)[default:no]: "
        confirm = raw_input(msg)
        while 1:
            if not confirm:
                return
            if confirm in ('yes', 'y', 'YES', 'Y'):
                break
            confirm = raw_input('Please enter either "yes" or "no": ')
            continue
        
        from django.core.management import call_command
        call_command("createdefaultsite", interactive=True)
        
signals.post_syncdb.connect(update_default_site, sender=site_app, dispatch_uid="django.contrib.site.site_default")

