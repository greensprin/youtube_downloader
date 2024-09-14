@echo off

set VIDEO_PATH=.\cut\output\cut.mp4
set TIMETABLE=.\cut\input\whisper_timetable.txt
set OUT_FILE=.\output\cut.exo

call python .\cut\movie_cut.py %VIDEO_PATH% %TIMETABLE% %OUT_FILE%