# pytubefix github
# https://github.com/JuanBindez/pytubefix
# pytubefix document
# https://pytubefix.readthedocs.io/en/latest/index.html

import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
import yaml
import re
import subprocess
import shutil

class YoutubeDonwloader:
    def __init__(self):
        # 設定ファイル読み込み
        with open("config.yaml", "r", encoding="utf-8", errors="ignore") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        # 各種設定取得
        self.url                    = config["url"]
        self.out_dir                = config["out_dir"]
        self.resolution             = config["resolution"]
        self.ext                    = config["ext"]
        self.concat_video_and_audio = config["concat_video_and_audio"]

        # 出力フォルダ作成
        if (os.path.exists(self.out_dir) == False):
            os.makedirs(self.out_dir)
    
    def run(self):
        # 動画URL設定
        yt = YouTube(self.url,
                     # use_oauth=True,
                     # allow_oauth_cache=True,
                     on_progress_callback=on_progress,
                     )

        # 動画タイトル取得
        title = yt.title
        print(title)

        # itag取得
        itag = self.__get_itag(yt)

        # 動画、音声ダウンロード
        self.__download(yt, itag)

        # 動画情報出力
        self.__output_info(self.url, title)

        print("[INFO] Done...")

    def __get_itag(self, yt):
        # 動画形式取得
        yt_filters = yt.streams.filter(res=f"{self.resolution}p")

        # 指定した動画解像度と拡張子からitagを取得する
        itag = 0
        for yt_filter in yt_filters:
            print(yt_filter)
            if (yt_filter.mime_type.find(self.ext) != -1):
                itag = yt_filter.itag
                break
            
        if (itag == 0):
            print("[ERROR] itag is not found.")
            quit()
        else:
            print(f"itag: {itag}")

        return itag

    def __download(self, yt, itag):
        # ys = yt.streams.get_highest_resolution()
        # ys.download(output_path=self.out_dir)

        # 動画ダウンロード
        print("[INFO] 動画をダウンロード中...")
        ys = yt.streams.get_by_itag(itag)
        ys.download(output_path=self.out_dir, filename=f"video.{self.ext}")

        # 音声ダウンロード (1080p以上だと動画と音声が別で保存されているため)
        if (self.resolution >= 1080):
            print("[INFO] 音声をダウンロード中...")
            ys = yt.streams.get_audio_only()
            ys.download(output_path=self.out_dir, mp3=True, filename="audio") # mp3=Trueの場合、filenameに拡張子はつけなくてよい

        # 動画と音声を合成する (ffmpegをコマンドラインで実行する方法にした(pythonライブラリ使う場合にどのようにcodecコピーするかわからなかったため))
        if (self.resolution >= 1080 and self.concat_video_and_audio == 1):
            print("[INFO] 動画と音声を合成中...")

            cmd = f"ffmpeg -i {self.out_dir}/video.webm \
                           -i {self.out_dir}/audio.mp3 \
                           -c copy \
                           -y \
                           {self.out_dir}/video.mp4"

            print(re.sub("\s+", " ", cmd)) # コード見やすいように改行や空白入れているので、コマンドライン表示時には削除する
            subprocess.run(cmd)

    def __output_info(self, url, title):
        with open(f"{self.out_dir}/info.txt", "w", encoding="utf-8", errors="ignore") as f:
            f.write(f"{url}\n")
            f.write(f"{title}\n")

if __name__ == "__main__":
    youtube_downloader = YoutubeDonwloader()
    youtube_downloader.run()