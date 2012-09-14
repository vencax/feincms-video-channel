feincms-video-channel
=====================

presents videos uploaded to a site in a channel manner, like youtube

youtube videos conversion
-------------------------

Simply browse to <your video page URL>/youtubeconv/ and fill in the form.
Do it whatever time you want. The videos will stack in a queue.
Then run ./manage.py downloadvideo to process the queue.

NOTE: you need youtube-dl somewhere in your path.
(https://github.com/rg3/youtube-dl/raw/2012.02.27/youtube-dl)

NOTE2: if you want seekable flv videos, you have to include special metadata.
This cam be done with tools like yamdi or flvtool2.
You must have also support for http pseudostreaming by your web server!
It shall understand requests with start GET param to be able to serve portions of video when seeked.
More about this topic on http://flowplayer.org/plugins/streaming/pseudostreaming.html.
