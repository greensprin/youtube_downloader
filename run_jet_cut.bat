@echo off

set VIDEO_PATH=.\cut\output\cut.mp4
set TIMETABLE=.\output\jet_cut_timetable.txt

call python .\jet_cut\jet_cut.py %VIDEO_PATH% %TIMETABLE%

set OUT_FILE=.\output\jet_cut.exo

call python .\cut\movie_cut.py %VIDEO_PATH% %TIMETABLE% %OUT_FILE%