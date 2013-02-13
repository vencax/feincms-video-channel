
import os
import subprocess
from django.template.defaultfilters import slugify


def videoPostSavedHandler(instance, created, **kwargs):
    """
    Converts FLV video file to form that can be
    served as pseudo http stram.
    """

    if created:
        orig = instance.mediaFile.file.file.name
        tmp = '%s.yamdiconverted' % orig
        p = subprocess.Popen(['yamdi', '-i', orig, '-o', tmp],
                             stderr=subprocess.PIPE)
        rv = p.wait()
        if rv == 0:
            os.remove(orig)
            os.rename(tmp, orig)
        else:
            os.remove(tmp)
            _, err = p.communicate()
            return err


def videoPreSavedHandler(instance, **kwargs):
    if not instance.slug:
        instance.slug = unicode(slugify(instance.mediaFile.translation))
