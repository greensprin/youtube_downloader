import os
import sys
import subprocess
from glob import glob
import re

def get_time(movie_time):
    hour    = int(movie_time // (60*60))
    minutes = int((movie_time - hour * (60*60)) // 60)
    sec     = (movie_time - hour * (60*60) - minutes * 60)

    return f"{hour:>02}:{minutes:>02}:{sec:>02}"

# 出力フォルダ作成
out_file = sys.argv[2]
out_dir = os.path.dirname(out_file)
if (os.path.exists(out_dir) == False):
    os.makedirs(out_dir)

# MP4ファイルから音声を抽出
input_video = sys.argv[1]
if (os.path.exists(f"{out_dir}/audio.mp3")):
    audio_output = f"{out_dir}/audio.mp3"
else:
    audio_output = f"{out_dir}/audio.wav"
    cmd = f"ffmpeg -i {input_video} -vn {audio_output} -y"
    subprocess.run(cmd, shell=True)

# == setting ===========================
noise            = -45
duration         = 0.5
keep_silence     = 0.25
silencedetect_en = 1
# ======================================

silencedetect_log = f"{out_dir}/silencedetect.log"
cmd = f"ffmpeg -i {audio_output} -af silencedetect=n={noise}dB:d={duration} -f null - 2> {silencedetect_log}"
print(cmd)
if (silencedetect_en == 1):
    subprocess.run(cmd, shell=True)

timetable_list = []
with open(silencedetect_log, "r", encoding="utf-8", errors="ignore") as f:
    movie_start_time = 0
    movie_end_time   = 0
    for line in f.readlines():
        silence_start = re.search("(?<=silence_start: )[0-9]+\.[0-9]+", line)
        silence_end   = re.search("(?<=silence_end: )[0-9]+\.[0-9]+"  , line)

        if (silence_start != None):
            movie_end_time = float(silence_start.group()) + keep_silence

            timetable_list.append(f"{get_time(movie_start_time)} - {get_time(movie_end_time)}")

            continue
        elif (silence_end != None):
            movie_start_time     = float(silence_end.group())
            movie_start_time_tmp = movie_start_time - keep_silence
            movie_start_time     = movie_start_time if (movie_start_time_tmp < movie_end_time) else movie_start_time_tmp
        else:
            pass

timetable_file = out_file
with open(timetable_file, "w", encoding="utf-8", errors="ignore") as f:
    f.writelines("\n".join(timetable_list))