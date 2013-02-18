# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
"""
Search for video files and encode them in format that can be served in
HTML5 video tag. (mp4, ogv, webm)
"""
import os
import logging
import subprocess
from django.conf import settings
from django.core.management.base import NoArgsCommand
from videochannel.models import Video
from videochannel.signals import prepareForPseudoStreaming


class Command(NoArgsCommand):
    help = 'Convert videos to be playable in flash.'  # @ReservedAssignment

    RESOLUTION = getattr(settings, 'FLV_RESOLUTION', '640x360')
    BITRATE = getattr(settings, 'FLV_BITRATE', '500')

    def handle_noargs(self, **options):
        vids = Video.objects.all()

        for m in vids:
            if 'flv' not in self._get_mime(m.mediaFile.file.file.name):
                self._processFile(m.mediaFile.file)

    def _processFile(self, mFile):
        logging.info('Processing %s ...' % mFile.file.name)
        ext = mFile.name.split('.')[-1]
        dest = '%sflv' % mFile.name.rstrip(ext)
        destFile = '%sflv' % mFile.file.name.rstrip(ext)
        try:
            self.encode_to_flv(mFile.file.name, destFile)
            prepareForPseudoStreaming(destFile)
            os.rename(mFile.file.name, '%s.old' % mFile.file.name)
            mFile.name = dest
            mFile.save()
        except Exception, e:
            logging.error(e)

    def _get_mime(self, mfile):
        p = subprocess.Popen(['file', mfile, '-ib'], stdout=subprocess.PIPE)
        return p.communicate()[0]

    def encode_to_flv(self, source, dest):
        if os.path.exists(dest):
            os.remove(dest)

        called = [
            'ffmpeg', '-i', source, '-vcodec', 'libx264',
            '-vpre', 'default', '-acodec', 'libmp3lame',
            '-ar', '44100', '-aq', '4', '-ac', '2', '-s', self.RESOLUTION,
            '-b', '%sk' % self.BITRATE,
            dest
        ]
        p = subprocess.Popen(called)
        rv = p.wait()
        if rv != 0:
            raise Exception(rv)
