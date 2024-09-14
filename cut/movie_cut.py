import sys
import re
import os

def get_frame(time):
    time_sp = time.split(":")

    hour   = int(time_sp[0])
    minute = int(time_sp[1])
    second = float(time_sp[2])

    frame = int((hour * (60**2) + minute * 60 + second) * 30)

    return frame

def gen_exo_format(movie_path, start_frame, end_frame, play_pos, num):
    frame_len = end_frame - start_frame

    movie = f'''
            [{num}]
            start={play_pos + 1}
            end={play_pos + frame_len}
            layer=1
            overlay=1
            camera=0
            [{num}.0]
            _name=動画ファイル
            再生位置={start_frame}
            再生速度=100.0
            ループ再生=0
            アルファチャンネルを読み込む=0
            file={movie_path}
            [{num}.1]
            _name=標準描画
            X=0.0
            Y=0.0
            Z=0.0
            拡大率=100.00
            透明度=0.0
            回転=0.00
            blend=0'''.replace(" ", "")

    music = f'''
            [{num+1}]
            start={play_pos + 1}
            end={play_pos + frame_len}
            layer=2
            overlay=1
            audio=1
            [{num+1}.0]
            _name=音声ファイル
            再生位置=0.00
            再生速度=100.0
            ループ再生=0
            動画ファイルと連携=1
            file={movie_path}
            [{num+1}.1]
            _name=標準再生
            音量=100.0
            左右=0.0'''.replace(" ", "")

    return f"{movie}{music}"

if __name__ == "__main__":
    # 動画のパスは絶対パスで指定する
    movie_path = sys.argv[1]
    movie_path = os.path.abspath(movie_path)
    # カット箇所指定のテキストファイル
    timetable  = sys.argv[2]
    play_pos   = 0

    out_file = sys.argv[3]
    out_dir = os.path.dirname(out_file)
    if (os.path.exists(out_dir) == False):
        os.makedirs(out_dir)

    with open(out_file, "w", encoding="shift-jis", errors="ignore") as fw:
        # headerを記述
        header = f'''[exedit]
                     width=1920
                     height=1080
                     rate=30
                     scale=1
                     length=309419
                     audio_rate=44100
                     audio_ch=2'''.replace(" ", "")
        fw.write(header)

        # timetableから時間取得して記載
        with open(timetable, "r", encoding="shift-jis", errors="ignore") as f:
            for i, line in enumerate(f.readlines()):
                line = line.replace("\n", "")
                line_sp = line.split()

                start_time = line_sp[0]
                end_time   = line_sp[2]
                # music_name = " ".join(line_sp[3:])
                # print(start_time, end_time) # , music_name)

                start_frame = get_frame(start_time) + 1
                end_frame   = get_frame(end_time)
                # print(start_frame, end_frame)

                exo_word = gen_exo_format(movie_path, start_frame, end_frame, play_pos, i*2)
                # print(exo_word)

                fw.write(exo_word)

                # 再生位置を移動する
                play_pos += (end_frame - start_frame)
                # print(play_pos)