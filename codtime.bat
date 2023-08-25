@echo off

REM Change directory to repo
cd /d "C:\Code\ajhalling\mwii-time-tracker"

REM Run refresh_data script to update .csv
cd dash\data
python ..\..\dash\scripts\refresh_data.py
cd ..

REM Add all changes (including the updated .csv file)
git add -A

REM Commit the changes with a message
git commit -m "Update: %date% from HTPC"

REM Set the HTTP header with the GITHUB_PAT environment variable
set "GIT_HTTP_HEADER=Authorization: Bearer %GITHUB_PAT%"

REM Push the changes to the remote repository (using 'main' as the branch name)
git push origin main
