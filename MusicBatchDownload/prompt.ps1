$url=(gc urls.txt)
$url|ForEach-Object -ThrottleLimit 8 -Parallel {yt-dlp.exe -f 30216 -x --audio-format mp3 $_ -o '%(title)s.%(ext)s'}
