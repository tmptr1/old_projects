import os
from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip
# pip install pytubefix
# pip install moviepy

def download_video(url):
    dir = r"videos/"
    tmp_dir = r"tmp_dir/"

    yt = YouTube(url)
    res = '1080p'

    stream = yt.streams.filter(progressive=True, resolution=res).first()
    # <Stream: itag="299" mime_type="video/mp4" res="1080p" fps="60fps" vcodec="avc1.64002a" progressive="False" sabr="False" type="video">,
    # stream = yt.streams.get_by_itag(251)
    # stream = yt.streams.get_highest_resolution()
    if stream:
        print(f"Downloading [{yt.title}] ...")
        stream.download(dir)
        print('Done')
        return

    stream = yt.streams.filter(resolution=res, type='video').first()
    if not stream:
        print(f"Для видео [{stream.title}] недоступно разрешение {res}")
        return

    print(f"Downloading [{yt.title}] (without audio) ...")
    video_tmp_file_path = stream.download(tmp_dir)
    print('Done')

    stream = yt.streams.filter(type='audio').order_by('abr').desc().first()
    print(f"Downloading [{yt.title}] (only audio) ...")
    audio_tmp_file_path = stream.download(tmp_dir)
    print('Done')

    video = VideoFileClip(video_tmp_file_path)
    audio = AudioFileClip(audio_tmp_file_path)

    final_video = video.with_audio(audio)
    final_video.write_videofile(fr"{dir}/{os.path.basename(video_tmp_file_path)}", codec='libx264', audio_codec='aac')

    video.close()
    audio.close()

    os.remove(video_tmp_file_path)
    os.remove(audio_tmp_file_path)
    print('Done')


if __name__ == '__main__':
    url = r"https://www.youtube.com/watch?v=abc"
    download_video(url)