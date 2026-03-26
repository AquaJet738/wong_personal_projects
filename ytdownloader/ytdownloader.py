import yt_dlp

def video_downloader(url, output="video-downloads"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def playlist_downloader(url, output="playlist-downloads"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output}/%(playlist)s/%(title)s.%(ext)s',
        'ignoreerrors': True,  # skip unavailable videos
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")

    if "playlist" in url:
        playlist_downloader(url)
    else:
        video_downloader(url)