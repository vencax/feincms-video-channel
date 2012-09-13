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

from django.conf import settings
from feincms import settings as fcms_settings
from django.core.management.base import NoArgsCommand
from videochannel.forms import CONV_INFO_FOLDER
from django.contrib.staticfiles import finders
from feincms.module.medialibrary.models import MediaFile, MediaFileTranslation

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
        subprocess.call(['mkdir', self.tmp])
        script = finders.find('videochannel/dowloadYT.sh')
        subprocess.call([script, url])
        
        for i in os.listdir(self.tmp):
            if i.endswith('.json'):
                with open(os.path.join(self.tmp, i)) as f:
                    now = datetime.datetime.now()
                    mediaPath = now.strftime(fcms_settings.FEINCMS_MEDIALIBRARY_UPLOAD_TO)
                    info = json.load(f)
                    vidFile = i.rstrip('.info.json')
                    self._processDownloadedFile(vidFile,
                                                info['title'], 
                                                info['description'], mediaPath)
                    if subtitlesURL:
                        self._downloadSubtitles(vidFile, subtitlesURL, mediaPath)
        subprocess.call(['rm', '-rf', self.tmp])
                    
    def _processDownloadedFile(self, vidfile, title, desc, mediaPath):
        orig = os.path.join(self.tmp, vidfile)
        new = os.path.join(settings.MEDIA_ROOT, mediaPath, vidfile)
        subprocess.call(['mv', orig, new])
        try:
            mf = MediaFile.objects.get(file=os.path.join(mediaPath, vidfile))
        except MediaFile.DoesNotExist:
            mf = MediaFile(file=os.path.join(mediaPath, vidfile))
        mf.save()
        tr = mf.get_translation()
        if tr == None:        
            tr = MediaFileTranslation(parent=mf, language_code='cs')
        tr.caption = title
        tr.description = desc
        tr.save()
        
    def _downloadSubtitles(self, vidFile, subtitlesURL, mediaPath):
        dest = os.path.join(settings.MEDIA_ROOT, mediaPath, '%s.srt' % vidFile)
        subprocess.call(['wget', '-O', dest, subtitlesURL])