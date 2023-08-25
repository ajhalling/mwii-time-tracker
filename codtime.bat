@echo off

REM change directory to repo
cd /d "C:\Code\ajhalling\mwii-time-tracker"

REM run refresh_data script to update .csv
python dash\scripts\refresh_data.py

REM Add all changes (including the updated local file)
git add -A

REM Commit the changes with a message
git commit -m "Update: %date% from HTPC"

REM Set the HTTP header with the GITHUB_PAT environment variable
set "GIT_HTTP_HEADER=Authorization: Bearer %GITHUB_PAT%"

REM Push the changes to the remote repository
git push origin master
