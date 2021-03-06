# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
"""
Search for video files and encode them in format that can be served in
HTML5 video tag. (mp4, ogv, webm)
"""

import os
import subprocess
import json
import pickle
import datetime
import glob
import sub2srt

from django.conf import settings
from feincms import settings as fcms_settings
from django.core.management.base import NoArgsCommand
from videochannel.forms import CONV_INFO_FOLDER
from django.contrib.staticfiles import finders
from feincms.module.medialibrary.models import MediaFile, MediaFileTranslation
from django.template.defaultfilters import mark_safe
import urllib2

class Command(NoArgsCommand):
    help = 'Download videos from well known video services.' #@ReservedAssignment
    infofolder = os.path.join(settings.MEDIA_ROOT, CONV_INFO_FOLDER)
    max_duration = 2 * 60 * 60 # 2 hours
    tmp = '/tmp/ee'

    def handle_noargs(self, **options):
        infoFiles = os.listdir(self.infofolder)
        begin = datetime.datetime.now()
        
        for i in infoFiles:
            # check if we have not run too long
            if (datetime.datetime.now() - begin).seconds > self.max_duration:
                return
            
            ifile = os.path.join(self.infofolder, i)
            with open(ifile, 'r') as f:
                videoURL, videoName, subtitlesURL = pickle.load(f)
            self._download(videoURL, videoName, subtitlesURL)
            os.remove(ifile)
        
    def _download(self, url, name, subtitlesURL):
        if not os.path.exists(self.tmp):
            os.mkdir(self.tmp)
        script = finders.find('videochannel/dowloadYT.sh')
        subprocess.call([script, url])
        if not glob.glob(os.path.join(self.tmp, '*.flv')):
            subprocess.call([script, url, '--all-formats'])
        
        try:
            flv = os.path.basename(glob.glob(os.path.join(self.tmp, '*.flv'))[0])
        except IndexError:
            return
        
        infoFile = os.path.join(self.tmp, '%s.info.json' % flv)
        with open(os.path.join(infoFile)) as f:
            now = datetime.datetime.now()
            mediaPath = now.strftime(fcms_settings.FEINCMS_MEDIALIBRARY_UPLOAD_TO)
            info = json.load(f)
            self._processDownloadedFile(flv,
                                        info['title'],
                                        info['description'], mediaPath)
            self._saveSplash(flv, info['thumbnail'], mediaPath)
            if subtitlesURL:
                self._downloadSubtitles(flv, subtitlesURL, mediaPath)
            else:
                self._saveYTSubtitles(info['id'], flv, mediaPath)
        subprocess.call(['rm', '-rf', self.tmp])
                    
    def _processDownloadedFile(self, vidFile, title, desc, mediaPath):
        orig = os.path.join(self.tmp, vidFile)
        new = os.path.join(settings.MEDIA_ROOT, mediaPath, vidFile)
        subprocess.call(['yamdi', '-i', orig, '-o', new])
        try:
            mf = MediaFile.objects.get(file=os.path.join(mediaPath, vidFile))
        except MediaFile.DoesNotExist:
            mf = MediaFile(file=os.path.join(mediaPath, vidFile))
        mf.save()
        tr = mf.get_translation()
        if tr == None:        
            tr = MediaFileTranslation(parent=mf, language_code='cs')
        tr.caption = mark_safe(title)
        tr.description = mark_safe(desc)
        tr.save()
        
    def _downloadSubtitles(self, vidFile, subtitlesURL, mediaPath):
        dest = self._get_subtitles_file(vidFile, mediaPath)
        subprocess.call(['wget', '-O', dest, subtitlesURL])
        
    def _get_subtitles_file(self, vidFile, mediaPath):
        return os.path.join(settings.MEDIA_ROOT, mediaPath, '%s.srt' % vidFile)
    
    def _saveSplash(self, vidFile, thumbURL, mediaPath):
        thumbMediaPath = os.path.join(mediaPath, '%s.jpg' % vidFile)
        
        thumbRealPath = os.path.join(settings.MEDIA_ROOT, thumbMediaPath)
        subprocess.call(['wget', '-O', thumbRealPath, thumbURL])
        
        try:
            mf = MediaFile.objects.get(file=thumbMediaPath)
        except MediaFile.DoesNotExist:
            mf = MediaFile(file=thumbMediaPath)
        mf.save()

    def _saveYTSubtitles(self, ID, vidFile, mediaPath):
        url = 'http://video.google.com/timedtext?hl=%(LANG)s&v=%(ID)s&lang=%(LANG)s'
        url = url % {'LANG': 'cs', 'ID': ID}
        destFile = self._get_subtitles_file(vidFile, mediaPath)
        try:
            r = urllib2.urlopen(url, timeout=3)
            if r.code == 200:
                savedFile = os.path.join(self.tmp, 'titles.txt')
                with open(savedFile, 'w') as f:
                    f.write(r.read())
                sub2srt.convert(savedFile, destFile)
        except Exception:
            pass
