# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
"""
Search for video files and encode them in format that can be served in
HTML5 video tag. (mp4, ogv, webm)
"""

from django.core.management.base import NoArgsCommand

from feincms.module.medialibrary.models import MediaFile
import os
from django.conf import settings
import subprocess
from django.contrib.staticfiles import finders

class Command(NoArgsCommand):
    help = 'Encode video files to be usable in HTML5 video tag.' #@ReservedAssignment
    wanted_variants = ('ogv', 'webm')

    def handle_noargs(self, **options):
        foundmedia = MediaFile.objects.filter(type__in=['video'])
        
        for m in foundmedia:
            missing = self._get_missing_variants(m.file)
            source = os.path.join(settings.MEDIA_ROOT, m.file.name)
            for typ, dest in missing:
                try:                    
                    getattr(self, 'encode_to_%s' % typ)(source, dest)
                except AttributeError:
                    pass
            
    def _get_missing_variants(self, medfile):
        missing = []
        for v in self.wanted_variants:
            var = os.path.join(settings.MEDIA_ROOT,
                               '%s.%s' % (medfile.name, v))
            if not os.path.exists(var):
                missing.append((v, var))
        return missing
                
    def encode_to_mp4(self, source, dest):
        pass
    
    def encode_to_webm(self, source, dest):
        cmd = 'sh %s %s %s' %\
            (finders.find('videochannel/mp4ToWebm.sh'), source, dest)
        subprocess.call(cmd.split(' '))
        
    def encode_to_ogv(self, source, dest):
        cmd = 'ffmpeg2theora %s -o %s' % (source, dest)
        subprocess.call(cmd.split(' '))