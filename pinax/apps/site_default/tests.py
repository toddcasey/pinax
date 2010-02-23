import unittest
from django.contrib.sites.models import Site
import sys

class UpdateSiteDomainNameTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testCreateDefaultSiteDomainName(self):
        _sid=1
        _domname="domaname232.asdf"
        _disname="What a name"

        from management.commands.createdefaultsite import Command
        c = Command()
        c.handle(domainname=_domname ,displayname=_disname)
        
        s2 = Site.objects.get(id=_sid)
        self.assertEquals(s2.domain, _domname)
        self.assertEquals(s2.name, _disname)
    
    def testCreateDefaultSiteDomainName2(self):
        _sid=1
        _domname="domaname232.asdf.cc"
        _disname="Changed Domain Name"

        from management.commands.createdefaultsite import Command
        c = Command()
        c.handle(domainname=_domname ,displayname=_disname)
        
        s2 = Site.objects.get(id=_sid)
        self.assertEquals(s2.domain, _domname)
        self.assertEquals(s2.name, _disname)
    
       
from django.db.models import signals
from management import update_default_site
from django.contrib.sites import models as site_app
        
signals.post_syncdb.disconnect(update_default_site, sender=site_app, dispatch_uid="django.contrib.site.site_default")

