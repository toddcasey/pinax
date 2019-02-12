"""
Management utility to create or update default site.
"""

import re
import sys
from optparse import make_option
from django.contrib.sites.models import Site
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _


DOMAIN_RE = re.compile(
    r'(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

def is_valid_domainname(value):
    if not DOMAIN_RE.search(value):
        raise exceptions.ValidationError(_('Enter a valid domain name.'))

def is_valid_displayname(value):
    pass
    
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sitedomainname', dest='domainname', default=None,
            help='Specifies the site domain name.'),
        make_option('--sitedisplayname', dest='displayname', default=None,
            help='Specifies the site display name.'),
    )
    help = 'Used to create a default site. Provide both --sitedomainname and --sitedisplayname to suppress prompt. Remember double quoting display name if necessary.'

    def handle(self, *args, **options):
        domainname = options.get('domainname', None)
        displayname = options.get('displayname', None)
        interactive = True
  
        # We need both arguments to supress prompt.
        if ( domainname and not displayname ) or ( not domainname and displayname ):
            raise CommandError("You must use both --sitedomainname and --sitedisplayname.")
        
        if domainname and displayname:
            interactive = False
            try:
                is_valid_domainname(domainname)
            except exceptions.ValidationError:
                raise CommandError("Invalid domain name.")
            try:
                is_valid_displayname(displayname)
            except exceptions.ValidationError:
                raise CommandError("Invalid display name.")

        if interactive:
            try:
                # Get domain name
                while 1:
                    if not domainname:
                        domainname = raw_input('Site domain name: ')
                    try:
                        is_valid_domainname(domainname)
                    except exceptions.ValidationError:
                        sys.stderr.write("Error: That domain name is invalid.\n")
                        domainname = None
                    else:
                        break
            
                # Get display name
                while 1:
                    if not displayname:
                        displayname = raw_input('Site display name: ')
                    try:                   
                        is_valid_displayname(displayname)
                    except exceptions.ValidationError:
                        sys.stderr.write("Error: That domain name is invalid.\n")
                        displayname = None
                    else:
                        break
                
            except KeyboardInterrupt:
                sys.stderr.write("\nOperation cancelled.\n")
                sys.exit(1)
        
        from django.conf import settings
        try:
            # use the SITE_ID from settings.py
            sid = settings.SITE_ID
        except:
            sys.stderr.write("Error: Unable to update site data because of invalid SITE_ID in settings.\n")
    
        #Use the existing site object, or create one with the SITE_ID.
        try:
            site = Site.objects.get(id=sid)
            site.domain = domainname
            site.name = displayname
        except:
            site = Site(id=sid, domain=domainname, name=displayname)
        
        #save the newly created, or modified site object
        try:
            site.save()
            Site.objects.clear_cache()
        except:
            sys.stderr.write("Error: Unable to save site data.\n")
            print(sys.exc_info())
        
