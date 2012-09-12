ffmpeg -pass 1 -passlogfile $1 -threads 4  -keyint_min 0 -g 250 -skip_threshold 0 -qmin 1 -qmax 51 -i $1 -vcodec libvpx -b 614400 -an -y -f webm /dev/null
ffmpeg -pass 2 -passlogfile $1 -threads 4  -keyint_min 0 -g 250 -skip_threshold 0 -qmin 1 -qmax 51 -i $1 -vcodec libvpx -b 614400 -acodec libvorbis -y $2
