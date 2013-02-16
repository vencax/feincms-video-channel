# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
"""
Search for video files and encode them in format that can be served in
HTML5 video tag. (mp4, ogv, webm)
"""
import os
import subprocess
from django.conf import settings
from django.core.management.base import NoArgsCommand
from videochannel.models import Video


class Command(NoArgsCommand):
    help = 'Convert videos to be playable in flash.'  # @ReservedAssignment

    def handle_noargs(self, **options):
        vids = Video.objects.all()

        for m in vids:
            src = m.mediaFile.file.file.name
            if 'flv' not in self._get_mime(src):
                ext = m.mediaFile.file.name.split('.')[-1]
                dest = '%sflv' % m.mediaFile.file.name.rstrip(ext)
                self.encode_to_flv(src, dest)
                os.rename(src, '%s.old' % src)
                m.mediaFile.file.name = dest
                m.mediaFile.save()

    def _get_mime(self, mfile):
        p = subprocess.Popen(['file', mfile, '-ib'], stdout=subprocess.PIPE)
        return p.communicate()[0]

    def _get_missing_variants(self, medfile):
        missing = []
        for v in self.wanted_variants:
            var = os.path.join(settings.MEDIA_ROOT,
                               '%s.%s' % (medfile.name, v))
            if not os.path.exists(var):
                missing.append((v, var))
        return missing

    def encode_to_flv(self, source, dest):
        if os.path.exists(dest):
            os.remove(dest)
        called = [
            'ffmpeg', '-i', source, '-vcodec', 'libx264',
            '-vpre', 'default', '-acodec', 'libmp3lame',
            '-ar', '44100', '-aq', '4', '-ac', '2', '-s', '640x360',
            '-b', '500k',
            dest
        ]
        print ' '.join(called)
        p = subprocess.Popen(called,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rv = p.wait()
        if rv != 0:
            raise Exception(p.communicate()[1])
        return rv
